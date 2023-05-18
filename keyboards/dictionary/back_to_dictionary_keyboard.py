from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_dict_kb():
    kb = InlineKeyboardBuilder()

    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="dictionary"))

    return kb.as_markup()
