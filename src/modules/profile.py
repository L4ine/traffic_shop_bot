import logging

from aiogram import Router, types, F

from data.strings import PROFILE_TEXT, ERROR_TEXT, NOT_BUYED_TEXT

from db.db_api import get_user

from modules.common.keyboard import get_back_menu
from modules.common.utils import get_config_file
from modules.common.xray import xray_client_exists


router = Router(name=__name__)


@router.callback_query(F.data == 'cb_profile')
async def start(callback: types.CallbackQuery):
	try:
		user = await get_user(callback.from_user.id)

		if not user.rent_expired_at:
			return callback.answer(NOT_BUYED_TEXT)

		client = await xray_client_exists(callback.from_user.id)

		await callback.message.edit_text(
			PROFILE_TEXT.format(
				date=user.rent_expired_at,
				config=get_config_file(
					callback.from_user.id,
					client['id']
				)
			),
			reply_markup=await get_back_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return callback.answer(ERROR_TEXT)
