from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def incr_visible_words_kb(code, type, flag_hide_1, flag_hide_5):
    buttons = list()
    if not flag_hide_1:
        buttons.append(
            types.InlineKeyboardButton(
                text=f"Show 1 more {type}", callback_data=f"print_words_{type}_1"
            )
        )
    if not flag_hide_5:
        buttons.append(
            types.InlineKeyboardButton(
                text=f"Show 5 more {type}", callback_data=f"print_words_{type}_5"
            )
        )

    kb = InlineKeyboardBuilder(
        [
            buttons,
            [
                types.InlineKeyboardButton(
                    text="⬅️ Back", callback_data=f"choose_dict_to_get_{code}"
                )
            ],
        ]
    )

    return kb.as_markup()
