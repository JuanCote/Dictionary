from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_dict_kb(languages):
    kb = InlineKeyboardBuilder()
    for language in languages:
        kb.add(
            types.InlineKeyboardButton(
                text=language["label"],
                callback_data=f"choose_dict_to_get_{language['code']}",
            )
        )
    kb.row(types.InlineKeyboardButton(text="Create new dictionary", callback_data="add_dictionary"))
    kb.add(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_main"))

    return kb.as_markup()
