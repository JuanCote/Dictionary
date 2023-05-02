from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_word_kb():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text="🚮 Delete word 🗑️", callback_data="delete_word")
    )

    return kb.as_markup()
