from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# The main KeyboardMarkup that appears at startup
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
add_btn = KeyboardButton('Add')
get_dictionary = KeyboardButton('Dictionary')
repeat_words = KeyboardButton('Repeat')
main_kb.add(add_btn).add(get_dictionary).add(repeat_words)
