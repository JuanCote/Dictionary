from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_action_kb(languages):
    kb = InlineKeyboardBuilder()
    for language in languages:
        kb.add(types.InlineKeyboardButton(
            text=language['label'],
            callback_data=f"choose_language_{language['label']}"
        ))

    kb.add(types.InlineKeyboardButton(
        text="⬅️ Back",
        callback_data="back_to_main"
    ))

    return kb.as_markup()
