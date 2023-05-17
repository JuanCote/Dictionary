from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def no_words_in_dict_kb(language_code: str):
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(
            text="Add new word ➕", callback_data=f"choose_dict_to_add_{language_code}"
        )
    )
    kb.row(types.InlineKeyboardButton(text="️⬅️ Back", callback_data="back_to_main"))

    return kb.as_markup()
