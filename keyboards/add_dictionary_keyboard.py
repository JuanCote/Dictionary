from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_dictionary_kb():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(
            text="⬅️ Add dictionary", callback_data="add_dictionary"
        )
    )

    return kb.as_markup()
