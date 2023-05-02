from functools import partial

from aiogram import Router, types, Bot
from aiogram.client import bot
from aiogram.filters import Text
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.add_word import languages
from handlers.start import MAIN_TEXT
from helpers import edit_message
from keyboards.delete_word import delete_word_kb
from keyboards.dictionary_keyboard import choose_dict_kb
from keyboards.main_keyboard import main_kb
from mongo_db import users

router = Router()


class FSMDeleteWord(StatesGroup):
    words = State()
    number = State()


@router.callback_query(Text("dictionary"))
async def choose_dictionary_language(callback: types.CallbackQuery, bot: Bot):
    await edit_message(
        bot=bot,
        callback=callback,
        message="📖 Choose dictionary language 👀",
        keyboard_fn=partial(choose_dict_kb, languages),
    )


@router.callback_query(lambda message: message.data.startswith("choose_dict"))
async def get_words_dictionary(
    callback: types.CallbackQuery, bot: Bot, state: FSMContext
):
    await state.set_state(FSMDeleteWord.words)
    language = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    try:
        user = users.find_one({"user_id": user_id})
        words = user["dictionary"]
        if words:
            result = ""
            delete_words = list()
            for inx, elem in enumerate(words):
                delete_words.append(elem)
                if elem["language_to"] == language:
                    word = elem["word"]
                    translate = elem["translate"]
                    result += f"{inx+1}. {word} - {translate}\n"
            if not result:
                await bot.send_message(
                    chat_id=chat_id, text="There are no words in this dictionary"
                )
            else:
                await state.update_data(words=delete_words)
                await bot.send_message(
                    chat_id=chat_id, text=result, reply_markup=delete_word_kb()
                )
        else:
            await bot.send_message(
                chat_id=chat_id, text="There are no words in this dictionary"
            )
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=chat_id, text="DB_ERROR", reply_markup=main_kb())
    await bot.send_message(chat_id=chat_id, text=MAIN_TEXT, reply_markup=main_kb())


@router.callback_query(
    FSMDeleteWord.words, lambda message: message.data.startswith("delete_word")
)
async def number_word(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMDeleteWord.number)
    chat_id = callback.message.chat.id
    await bot.send_message(
        chat_id=chat_id, text="Enter the number of the word you want to delete"
    )


@router.message(FSMDeleteWord.number)
async def delete_word(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    data = await state.get_data()
    words = data["words"]
    if (
        not message.text.isdigit()
        or int(message.text) > len(words)
        or int(message.text) == 0
    ):
        await message.answer(
            text="You should enter a number that should indicate a word in the dictionary"
        )
    else:
        number = int(message.text)
        try:
            users.update_one(
                {"user_id": user_id}, {"$pull": {"dictionary": words[number - 1]}}
            )
            await message.answer(text="The word has been removed from the dictionary")
            await message.answer(text=MAIN_TEXT, reply_markup=main_kb())
        except Exception as e:
            print(e)
            await message.answer(text="DB ERROR")
            await message.answer(text=MAIN_TEXT, reply_markup=main_kb())
