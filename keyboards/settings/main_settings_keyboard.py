from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_settings_kb(is_auto_translate_enable: bool):
    kb = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(
                    text=f"️🤖 Auto translate - {'on' if is_auto_translate_enable else 'off'}",
                    callback_data="change_settings_auto-translate",
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="🗑️ Delete dictionary", callback_data="dict_delete"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="⬅️ Back", callback_data="back_to_main"
                ),
            ],
        ]
    )
    return kb.as_markup()
