from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ask_translate_kb():
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(text="👍 Agree", callback_data='agree_translate'),
                types.InlineKeyboardButton(text="😕 Your own translation", callback_data='disagree_translate'),
            ],
            [
                types.InlineKeyboardButton(text="Cancel 🙉", callback_data='add_word')
            ]
        ]
    )
    return kb.as_markup()
