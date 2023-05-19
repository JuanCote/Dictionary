from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_add_word_kb(to: str = "add_word"):
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="🙉 Cancel", callback_data=to))
    return kb.as_markup()
