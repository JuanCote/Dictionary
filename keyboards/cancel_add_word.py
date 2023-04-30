from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_add_word_kb():
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Cancel 🙉", callback_data="add_word"))
    return kb.as_markup()
