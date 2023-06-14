from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ask_native_word_kb():
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(text="Add a list of words 📋", callback_data='add_list'),
            ],
            [
                types.InlineKeyboardButton(text="Cancel 🙉", callback_data='add_word')
            ]
        ]
    )
    return kb.as_markup()
