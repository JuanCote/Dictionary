from aiogram import Bot, Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

from helpers import edit_message
from keyboards.main_keyboard import main_kb

router = Router()

MAIN_TEXT = 'Hello 👋\nThis is custom dictionary bot 📖'


@router.message(Command('start'))
async def start(message: types.Message, bot: Bot):
    await message.answer(text=MAIN_TEXT, reply_markup=main_kb())


@router.callback_query(Text("back_to_main"))
async def back_to_main(callback: types.CallbackQuery, bot: Bot):

    await edit_message(callback=callback, bot=bot, keyboard_fn=main_kb, message=MAIN_TEXT)

# from random import randint
# from aiogram import types
# from buttons import main_kb
# from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
# from aiogram.filters.command import Command
# from aiogram.filters.text import Text
# from create_bot import dp
# from buttons import main_kb, languages_kb
# from mongo_db import dictionary
# class FSMAddWord(StatesGroup):
#     language = State()
#     en_word = State()
#     lang_word = State()
# @dp.message_handler(commands=['add'])
# async def add_word(message: types.Message):
#     await FSMAddWord.language.set()
#     await message.answer('Choose language', reply_markup=languages_kb)
# @dp.message_handler(state=FSMAddWord.language)
# async def choose_language(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['language'] = message.text
#     await FSMAddWord.next()
#     await message.answer('Write a word in English', reply_markup=ReplyKeyboardRemove())
# @dp.message_handler(state=FSMAddWord.en_word)
# async def en_word(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['en_word'] = message.text
#         language = data['language']
#     await FSMAddWord.next()
#     await message.answer(f'Write a word in {language}')
# @dp.message_handler(state=FSMAddWord.lang_word)
# async def lang_word(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         user_id = message.from_user.id
#         language = data['language']
#         new_word_en = data['en_word']
#         new_word_lang = message.text
#         print(new_word_lang)
#         try:
#             user_filter = {'language': language,
#                            f'users.{user_id}': {'$exists': True}}
#             record = dictionary.find_one(user_filter)
#             if record:
#                 user_dictionary = record['users'][str(user_id)]
#                 if new_word_en in user_dictionary:
#                     await message.answer('This word is already in the dictionary')
#                 else:
#                     user_dictionary[new_word_en] = new_word_lang
#                     dictionary.update_one(user_filter,
#                                           {'$set': {f'users.{user_id}': user_dictionary}})
#                     await message.answer('The word was added successfully', reply_markup=main_kb)
#             else:
#                 dictionary.update_one({'language': language}, {
#                                       '$set': {f'users.{user_id}': {new_word_en: new_word_lang}}})
#                 await message.answer('The word was added successfully', reply_markup=main_kb)
#         except:
#             await message.answer('Database Error')
#         await state.finish()
