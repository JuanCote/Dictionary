from aiogram import Bot, Router, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functools import partial
from handlers.start import MAIN_TEXT

from helpers import edit_message, get_dictionaries, languages_codes
from keyboards.add_dictionary_keyboard import add_dictionary_kb
from keyboards.add_word.add_word_keyboard import add_action_kb
from keyboards.main_keyboard import main_kb
from keyboards.add_word.validate_add_word_keyboard import validate_add_word
from mongo_db import users

router = Router()


class FSMAddWord(StatesGroup):
    word = State()
    check_input = State()
    add_to_db = State()


@router.callback_query(Text("add_word"))
async def add_word(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    dictionaries = get_dictionaries(user_id)
    if not dictionaries:
        await edit_message(
            bot=bot,
            callback=callback,
            message="📖 You don't have any dictionaries yet, please add some 👀",
            keyboard_fn=add_dictionary_kb,
        )
    else:
        await edit_message(
            bot=bot,
            callback=callback,
            message="Choose dictionary 🇺🇳",
            keyboard_fn=partial(add_action_kb, dictionaries),
        )


@router.callback_query(lambda message: message.data.startswith("choose_dict_to_add"))
async def choose_language(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    code = callback.data.split("_")[-1]
    for elem in languages_codes:
        if code in languages_codes[elem]:
            label = languages_codes[elem][code]
    await state.update_data(code=code, label=label)
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
    await message.answer(
        text=f"Now write a translation in <b>{data['label']}</b>",
        parse_mode="HTML",
    )


@router.message(FSMAddWord.check_input)
async def check_input(message: types.Message, state: FSMContext):
    await state.update_data(translate=message.text)
    data = await state.get_data()
    await state.set_state(FSMAddWord.add_to_db)
    await message.answer(
        text=f"Check up all your data?\n"
        + f"Selected dictionary: <b>{data['label']}</b>\n"
        + f"Word in native language: <b>{data['word']}</b>\n"
        + f"Translation: <b>{data['translate']}</b>",
        parse_mode="HTML",
        reply_markup=validate_add_word(),
    )


@router.callback_query(FSMAddWord.add_to_db, Text("add_word_db"))
async def choose_word(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data_to_push = {"word": data["word"], "translate": data["translate"]}
    user_id = callback.from_user.id
    try:
        users.update_one(
            {"user_id": user_id},
            {"$push": {f"dictionaries.{data['code']}": data_to_push}},
        )
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
