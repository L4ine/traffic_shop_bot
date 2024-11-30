import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from data.config import TARIFFS
from data.strings import BUY_TEXT, PAY_TEXT, BILL_TEXT, \
	ERROR_PAY_TEXT, SUCCESS_PAY_TEXT, ERROR_TEXT

from db.db_api import add_payment, update_payment_status, \
	update_user_rent_expired, get_payment

from modules.common.keyboard import get_back_menu, get_buy_menu, get_pay_menu
from modules.common.payment import create_payment, check_payment
from modules.common.xray import add_xray_client, xray_client_exists, \
	update_xray_duration
from modules.common.utils import get_config_file


router = Router(name=__name__)


@router.callback_query(F.data == 'cb_buy')
async def buy(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			BUY_TEXT,
			reply_markup=await get_buy_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)


@router.callback_query(F.data == 'cb_back_buy')
async def bsck_buy(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			BUY_TEXT,
			reply_markup=await get_buy_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)


@router.callback_query(F.data.startswith('cb_buy_'))
async def pay(callback: types.CallbackQuery):
	try:
		period = int(callback.data.split('_')[-1])
		period_name = TARIFFS[period]['name']
		period_amount = TARIFFS[period]['amount']

		payment = await create_payment(
			amount=period_amount,
			description=BILL_TEXT.format(period=period_name)
		)

		await add_payment(
			tg_id=callback.from_user.id,
			payment_id=payment.id,
			amount=period_amount,
			period=period
		)

		await callback.message.edit_text(
			PAY_TEXT.format(
				period=period_name
			),
			reply_markup=await get_pay_menu(
				payment.confirmation.confirmation_url,
				payment.id
			)
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)


@router.callback_query(F.data.startswith('cb_check_'))
async def check_bill(callback: types.CallbackQuery, state: FSMContext):
	try:
		data = await state.get_data()

		if data.get('is_checking'):
			return callback.answer(ERROR_PAY_TEXT)

		await state.update_data(is_checking=True)

		payment_id = callback.data.split('_')[-1]
		payment = await get_payment(payment_id)
		status = await check_payment(payment_id)

		if not status:
			return callback.answer(ERROR_PAY_TEXT)

		await update_payment_status(
			payment_id=payment_id,
			status=True
		)

		client = await xray_client_exists(callback.from_user.id)

		if client:
			await update_xray_duration(
				tg_id=callback.from_user.id,
				client=client,
				days=payment.period * 30
			)
		else:
			client = await add_xray_client(
				tg_id=callback.from_user.id,
				days=payment.period * 30
			)

		await update_user_rent_expired(
			tg_id=callback.from_user.id,
			days=payment.period * 30
		)

		await callback.message.edit_text(
			SUCCESS_PAY_TEXT.format(
				config=get_config_file(
					callback.from_user.id,
					client['id'])
			),
			reply_markup=await get_back_menu()
		)

		await state.clear()

	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)
