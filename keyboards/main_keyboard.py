from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb():
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text="➕ Add word to dictionary", callback_data="add_word"
        ),
    )
    kb.row(types.InlineKeyboardButton(text="📖 Dictionary", callback_data="dictionary"))
    kb.row(types.InlineKeyboardButton(text="⚙️ Settings", callback_data="settings"))
    return kb.as_markup()


# main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# add_btn = KeyboardButton('/Add')
# get_dictionary = KeyboardButton('/Dictionary')
# repeat_words = KeyboardButton('/Repeat')
# main_kb.add(add_btn).add(get_dictionary).insert(repeat_words)

# languages_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# russian_btn = KeyboardButton('Russian')
# spanish_btn = KeyboardButton('Spanish')
# languages_kb.add(russian_btn).add(spanish_btn)
