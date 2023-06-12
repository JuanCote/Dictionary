from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def check_delete_dict_kb(dict_code: str):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="✅ Sure", callback_data=f"dict_delete_{dict_code}"))
    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="dict_delete"))

    return kb.as_markup()