from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_action_kb(languages):
    kb = InlineKeyboardBuilder()
    for i, language in enumerate(languages):
        kb.add(
            types.InlineKeyboardButton(
                text=language["label"],
                callback_data=f"choose_language_{i}",
            )
        )

    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_main"))

    return kb.as_markup()
