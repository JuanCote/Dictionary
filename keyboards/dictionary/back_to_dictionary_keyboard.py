from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_dict_kb(code):
    kb = InlineKeyboardBuilder()

    kb.row(
        types.InlineKeyboardButton(
            text="⬅️ Back", callback_data=f"choose_dict_to_get_{code}"
        )
    )

    return kb.as_markup()
