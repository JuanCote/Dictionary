from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def table_style_kb():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Plain table", callback_data="print_words_plain"))
    kb.add(types.InlineKeyboardButton(text="Invisible translate", callback_data="print_words_translate"))
    kb.add(types.InlineKeyboardButton(text="Invisible word", callback_data="print_words_word"))
    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="dictionary"))

    return kb.as_markup()
