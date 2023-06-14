from aiogram import Bot, Router, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functools import partial
from handlers.start import MAIN_TEXT

from helpers import edit_message, get_dictionaries, languages_codes, translate_word
from keyboards.add_dictionary.add_dictionary_keyboard import add_dictionary_kb
from keyboards.add_word.add_word_keyboard import add_action_kb
from keyboards.add_word.ask_native_word_keyboard import ask_native_word_kb
from keyboards.add_word.ask_translate_keyboard import ask_translate_kb
from keyboards.cancel_keyboard import cancel_kb
from keyboards.main_keyboard import main_kb
from keyboards.add_word.validate_add_word_keyboard import validate_add_word
from mongo_db import users

router = Router()


class FSMAddWord(StatesGroup):
    auto_translate_off = State()
    ask_translate = State()
    check_input = State()
    add_list = State()


@router.callback_query(Text("add_word"))
async def add_word(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    dictionaries = get_dictionaries(user_id)
    if not dictionaries:
        await edit_message(
            bot=bot,
            callback=callback,
            message="You don't have any dictionaries yet, please add some 👀",
            keyboard_fn=add_dictionary_kb,
        )
    else:
        await edit_message(
            bot=bot,
            callback=callback,
            message="🇺🇳 Choose dictionary",
            keyboard_fn=partial(add_action_kb, dictionaries),
        )


@router.callback_query(lambda message: message.data.startswith("choose_dict_to_add"))
async def choose_language(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    code = callback.data.split("_")[-1]
    for elem in languages_codes:
        if code in languages_codes[elem]:
            label = languages_codes[elem][code]
    await state.update_data(code=code, label=label)
    settings = users.find_one({"user_id": user_id})["settings"]
    if settings["auto_translate"]:
        await state.set_state(FSMAddWord.ask_translate)
    else:
        await state.set_state(FSMAddWord.auto_translate_off)
    await edit_message(
        bot=bot,
        callback=callback,
        message="Write a word in your native language ⭐️",
        keyboard_fn=ask_native_word_kb,
    )


@router.callback_query(Text("add_list"))
async def add_list_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(FSMAddWord.add_list)
    await edit_message(
        bot=bot,
        callback=callback,
        message="Write a list of word pairs in the format:\nword-translation\nword-translation\nMake sure to have a new line between each pair",
        keyboard_fn=partial(cancel_kb, 'add_word'),
    )


@router.message(FSMAddWord.add_list)
async def add_list_state(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    pairs_list = message.text.strip().split('\n')
    list_to_push = list()
    for pair in pairs_list:
        pair_list = pair.split('-')
        if len(pair_list) != 2:
            await message.answer(
                text='Wrong list',
                reply_markup=main_kb(),
            )
            return
        word, translate = pair_list[0].strip(), pair_list[1].strip()
        list_to_push.append({"word": word, "translate": translate})
    users.update_one(
        {"user_id": user_id},
        {"$push": {f"dictionaries.{data['code']}": {'$each': list_to_push}}},
    )
    await message.answer(
        text=MAIN_TEXT,
        reply_markup=main_kb(),
    )


@router.message(FSMAddWord.ask_translate)
async def ask_translate(message: types.Message, state: FSMContext):
    word = message.text.strip()
    data = await state.get_data()
    translate = translate_word(to_lang=data["code"], word=word)
    await state.update_data(word=word, translate=translate)
    await message.answer(
        text=f"Automatic translation - {translate}",
        parse_mode="HTML",
        reply_markup=ask_translate_kb(),
    )


@router.message(FSMAddWord.auto_translate_off)
async def auto_translate_off(message: types.Message, state: FSMContext):
    word = message.text.strip()
    await state.update_data(word=word)
    await state.set_state(FSMAddWord.check_input)
    data = await state.get_data()
    await message.answer(
        text=f"Now write a translation in <b>{data['label']}</b>",
        parse_mode="HTML",
        reply_markup=cancel_kb("add_word"),
    )


@router.callback_query(Text("disagree_translate"))
async def disagree_translate(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await state.set_state(FSMAddWord.check_input)
    data = await state.get_data()
    await edit_message(
        bot=bot,
        callback=callback,
        message=f"Now write a translation in <b>{data['label']}</b>",
        keyboard_fn=partial(cancel_kb, "add_word"),
    )


@router.callback_query(Text("agree_translate"))
async def agree_translate(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await edit_message(
        bot=bot,
        callback=callback,
        message=f"Check up all your data?\n"
        + f"Selected dictionary: <b>{data['label']}</b>\n"
        + f"Word in native language: <b>{data['word']}</b>\n"
        + f"Translation: <b>{data['translate']}</b>",
        parse_mode="HTML",
        keyboard_fn=validate_add_word,
    )


@router.message(FSMAddWord.check_input)
async def check_input(message: types.Message, state: FSMContext):
    await state.update_data(translate=message.text)
    data = await state.get_data()
    await message.answer(
        text=f"Check up all your data?\n"
        + f"Selected dictionary: <b>{data['label']}</b>\n"
        + f"Word in native language: <b>{data['word']}</b>\n"
        + f"Translation: <b>{data['translate']}</b>",
        parse_mode="HTML",
        reply_markup=validate_add_word(),
    )


@router.callback_query(Text("add_word_db"))
async def add_to_db(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data_to_push = {"word": data["word"], "translate": data["translate"]}
    user_id = callback.from_user.id
    users.update_one(
        {"user_id": user_id},
        {"$push": {f"dictionaries.{data['code']}": data_to_push}},
    )
    await callback.answer(text="The word was successfully added 🥳")
    await edit_message(
        message=MAIN_TEXT,
        keyboard_fn=main_kb,
        bot=bot,
        callback=callback,
    )
    # End of work with state
    await state.clear()
