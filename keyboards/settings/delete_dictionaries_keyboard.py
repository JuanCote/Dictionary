from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_dict_kb(languages):
    kb = InlineKeyboardBuilder()
    for language in languages:
        kb.add(
            types.InlineKeyboardButton(
                text=language["label"],
                callback_data=f"check_delete_dict_{language['code']}"
            )
        )
    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="settings"))

    return kb.as_markup()