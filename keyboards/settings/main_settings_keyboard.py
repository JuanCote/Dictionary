from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_settings_kb():
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(text="🗑️ Delete dictionary", callback_data='dict_delete'),
            ],
            [
                types.InlineKeyboardButton(text="⬅️ Back to menu", callback_data='back_to_main'),
            ]
        ]
    )
    return kb.as_markup()
