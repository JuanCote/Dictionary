from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def table_output_kb(code):
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(
                    text="⬅️ Back", callback_data=f"choose_dict_to_get_{code}"
                ),
            ],
            
        ]
    )
    kb.row()

    return kb.as_markup()
