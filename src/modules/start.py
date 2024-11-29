import logging

from aiogram import Router, types, F
from aiogram.filters import Command

from data.strings import START_TEXT, ERROR_TEXT, HELP_TEXT

from db.db_api import user_exists, add_user

from modules.common.filters import ChatTypeFilter
from modules.common.keyboard import get_start_menu, get_back_menu


router = Router(name=__name__)


@router.message(Command('start'), ChatTypeFilter('private'))
async def start(message: types.Message):
	try:
		if not await user_exists(message.from_user.id):
			await add_user(
				message.from_user.id,
				message.from_user.username,
				message.from_user.first_name,
				message.from_user.last_name,
			)

		await message.answer(
			START_TEXT,
			reply_markup=await get_start_menu()
		)
	except Exception as exc:
		logging.error(exc)


@router.callback_query(F.data == 'cb_back')
async def back(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			START_TEXT,
			reply_markup=await get_start_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)


@router.callback_query(F.data == 'cb_help')
async def back(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			HELP_TEXT,
			reply_markup=await get_back_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)
