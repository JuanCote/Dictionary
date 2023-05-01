import asyncio
from datetime import datetime

from aiogram import Bot, Router, types, F
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functools import partial
from handlers.start import MAIN_TEXT

from helpers import edit_message
from keyboards.add_keyboard import add_action_kb
from keyboards.cancel_add_word import cancel_add_word_kb
from keyboards.main_keyboard import main_kb
from keyboards.validate_add_word import validate_add_word
from mongo_db import users

router = Router()


class FSMAddWord(StatesGroup):
    language = State()
    word = State()
    check_input = State()
    add_to_db = State()


languages = (
    {"value": "RU", "label": "Russian 🇷🇺"},
    {"value": "SP", "label": "Spanish 🇪🇸"},
)


@router.callback_query(Text("add_word"))
async def add_word(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(FSMAddWord.language)
    await edit_message(
        bot=bot,
        callback=callback,
        message="Choose dictionary language 🇺🇳",
        keyboard_fn=partial(add_action_kb, languages),
    )


@router.callback_query(
    FSMAddWord.language, lambda message: message.data.startswith("choose_language")
)
async def choose_language(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.update_data(language_to=int(callback.data.split("_")[-1]))
    await state.set_state(FSMAddWord.word)
    await edit_message(
        bot=bot,
        callback=callback,
        message="Write a word in your native language ⭐️",
    )


@router.message(FSMAddWord.word)
async def choose_word(message: types.Message, state: FSMContext):
    await state.update_data(word=message.text.strip())
    await state.set_state(FSMAddWord.check_input)
    data = await state.get_data()
    language = languages[data["language_to"]]
    await message.answer(
        text=f"Now write a translation in <b>{language['label']}</b>",
        parse_mode="HTML",
    )


@router.message(FSMAddWord.check_input)
async def check_input(message: types.Message, state: FSMContext):
    await state.update_data(translate=message.text)
    data = await state.get_data()
    language = languages[data["language_to"]]
    await state.set_state(FSMAddWord.add_to_db)
    await message.answer(
        text=f"Check up all your data?\n"
        + f"Selected dictionary language: <b>{language['label']}</b>\n"
        + f"Word in native language: <b>{data['word']}</b>\n"
        + f"Translation: <b>{data['translate']}</b>",
        parse_mode="HTML",
        reply_markup=validate_add_word(),
    )


@router.callback_query(FSMAddWord.add_to_db, Text("add_word_db"))
async def choose_word(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = callback.from_user.id
    uuid = int(str(datetime.now().timestamp()).replace(".", ""))
    data["uuid"] = uuid
    try:
        users.update_one({"user_id": user_id}, {"$push": {"dictionary": data}})
        await callback.answer(text="The word was successfully added 🥳")
    except:
        await callback.answer(text="DB ERROR")

    await edit_message(
        message=MAIN_TEXT,
        keyboard_fn=main_kb,
        bot=bot,
        callback=callback,
    )
    # End of work with state
    await state.clear()
