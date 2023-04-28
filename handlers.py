from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from buttons import main_kb, languages_kb
from mongo_db import dictionary, MONGODB_URI


class FSMAddWord(StatesGroup):
    language = State()
    en_word = State()
    lang_word = State()


async def start(message: types.Message):

    await message.answer('', reply_markup=main_kb)


async def add_word(message: types.Message):
    await FSMAddWord.language.set()
    await message.answer('Choose language', reply_markup=languages_kb)


async def choose_language(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = message.text
    await FSMAddWord.next()
    await message.answer('Write a word in English', reply_markup=ReplyKeyboardRemove())


async def en_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['en_word'] = message.text
        language = data['language']
    await FSMAddWord.next()
    await message.answer(f'Write a word in {language}')


async def lang_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        language = data['language']
        new_word_en = data['en_word']
        new_word_lang = message.text
        print(new_word_lang)
        try:
            user_filter = {'language': language, f'users.{user_id}': {'$exists': True}}
            record = dictionary.find_one(user_filter)
            if record:
                user_dictionary = record['users'][str(user_id)]
                if new_word_en in user_dictionary:
                    await message.answer('This word is already in the dictionary')
                else:
                    user_dictionary[new_word_en] = new_word_lang
                    dictionary.update_one(user_filter,
                                          {'$set': {f'users.{user_id}': user_dictionary}})
                    await message.answer('The word was added successfully', reply_markup=main_kb)
            else:
                dictionary.update_one({'language': language}, {'$set': {f'users.{user_id}': {new_word_en: new_word_lang}}})
                await message.answer('The word was added successfully', reply_markup=main_kb)
        except:
            await message.answer('Database Error')
        await state.finish()




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(add_word, commands=['add'], state=None)
    dp.register_message_handler(choose_language, state=FSMAddWord.language)
    dp.register_message_handler(en_word, state=FSMAddWord.en_word)
    dp.register_message_handler(lang_word, state=FSMAddWord.lang_word)

