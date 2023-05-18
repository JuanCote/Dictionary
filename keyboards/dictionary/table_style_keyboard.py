from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def table_style_kb():
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(
                    text="Plain table", callback_data="print_words_plain_0"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Hide translation", callback_data="print_words_translate_0"
                ),
                types.InlineKeyboardButton(
                    text="Hide word", callback_data="print_words_word_0"
                ),
            ],
            [types.InlineKeyboardButton(text="⬅️ Back", callback_data="dictionary")],
        ]
    )
    # kb.add())
    # kb.add() # kb.row()

    return kb.as_markup()
