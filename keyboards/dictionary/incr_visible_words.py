from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def incr_visible_words_kb(code, type):
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(
                    text=f"Show 1 more {type}", callback_data=f"print_words_{type}_1"
                ),
                types.InlineKeyboardButton(
                    text=f"Show 5 more {type}", callback_data=f"increment_{type}_5"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="⬅️ Back", callback_data=f"choose_dict_to_get_{code}"
                )
            ],
        ]
    )

    return kb.as_markup()
