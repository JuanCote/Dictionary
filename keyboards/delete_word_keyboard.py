from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_word_kb(language_code: str):
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(
            text="Delete word 🗑️", callback_data=f"delete_words_{language_code}"
        ),
        types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_main"),
    )

    return kb.as_markup()
