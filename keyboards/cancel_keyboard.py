from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_kb(to):
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Cancel 🙉", callback_data=to))
    return kb.as_markup()
