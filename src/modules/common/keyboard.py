from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.config import TARIFFS
from data.strings import BUY_BUTTON, PROFILE_BUTTON, SUPPORT_BUTTON, \
	BACK_BUTTON, PAY_BUTTON, CHECK_BUTTON, HELP_BUTTON


async def get_start_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		types.InlineKeyboardButton(
			text=BUY_BUTTON,
			callback_data="cb_buy"
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=PROFILE_BUTTON,
			callback_data="cb_profile"
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=HELP_BUTTON,
			callback_data="cb_help"
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=SUPPORT_BUTTON,
			url="https://t.me/By_03"
		)
	)
	return builder.as_markup()


async def get_buy_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()

	for period, info in TARIFFS.items():
		builder.row(
			types.InlineKeyboardButton(
				text=f"{info['name']} - {info['amount']} руб.",
				callback_data=f"cb_buy_{period}"
			)
		)
	builder.row(
		types.InlineKeyboardButton(
			text=BACK_BUTTON,
			callback_data='cb_back'
		)
	)

	return builder.as_markup()


async def get_pay_menu(
	url: str,
	payment_id: str
) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		types.InlineKeyboardButton(
			text=PAY_BUTTON,
			url=url
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=CHECK_BUTTON,
			callback_data=f"cb_check_{payment_id}"
		)
	)

	return builder.as_markup()


async def get_back_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=BACK_BUTTON,
		callback_data='cb_back'
	)
	return builder.as_markup()
