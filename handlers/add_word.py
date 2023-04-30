import asyncio
from aiogram import Bot, Router, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functools import partial
from handlers.start import MAIN_TEXT

from helpers import edit_message
from keyboards.add_keyboard import add_action_kb
from keyboards.cancel_add_word import cancel_add_word_kb
from keyboards.main_keyboard import main_kb

router = Router()


class FSMAddWord(StatesGroup):
    language = State()
    word = State()
    translate = State()


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
    await state.update_data(language=callback.data.split("_")[-1])
    await state.set_state(FSMAddWord.word)

    await edit_message(
        bot=bot,
        callback=callback,
        message="Write a word in your native language ⭐️",
        keyboard_fn=cancel_add_word_kb,
    )


@router.message(FSMAddWord.word)
async def choose_word(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(word=message.text)
    await state.set_state(FSMAddWord.translate)
    data = await state.get_data()
    language = data["language"]
    await message.answer(
        text=f"Now write a translation in <b>{language.lower()}</b>",
        reply_markup=cancel_add_word_kb(),
        parse_mode="HTML",
    )


@router.message(FSMAddWord.translate)
async def choose_word(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(translate=message.text)
    data = await state.get_data()
    word, language = data["word"], data["language"]
    print(await state.get_data())
    await message.answer(text="The word was successfully added 🥳")
    await message.answer(text="Choose what you wanna do next 👀", reply_markup=main_kb())
    # End of work with state
    await state.clear()
