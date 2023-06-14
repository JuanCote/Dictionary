from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def validate_add_word():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(
            text="👌 My data is correct", callback_data="add_word_db"
        )
    )
    kb.row(
        types.InlineKeyboardButton(text="️🙈 I made a mistake", callback_data="add_word")
    )

    return kb.as_markup()
