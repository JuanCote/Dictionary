from functools import partial
from tabulate import tabulate
from aiogram import Router, types, Bot
from aiogram.utils import markdown as md
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from helpers import (
    edit_message,
    get_dictionaries,
)
from keyboards.dictionary.back_to_dictionary_keyboard import back_to_dict_kb
from keyboards.dictionary.dictionary_keyboard import choose_dict_kb
from keyboards.dictionary.table_style_keyboard import table_style_kb
from keyboards.main_keyboard import main_kb
from keyboards.add_dictionary_keyboard import add_dictionary_kb
from keyboards.dictionary.no_words_in_dictionary_keyboard import no_words_in_dict_kb
from mongo_db import users


DASH_LENGTH = 52

ROOM_FOR_ONE_WORD = 31

first_word = "WORD"

second_word = "TRANSLATION"

router = Router()


class FSMDeleteWord(StatesGroup):
    print = State()
    number = State()


@router.callback_query(Text("dictionary"))
async def choose_dictionary_language(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
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
            message="📖 Choose dictionary 👀",
            keyboard_fn=partial(choose_dict_kb, dictionaries),
        )


@router.callback_query(lambda message: message.data.startswith("choose_dict_to_get"))
async def get_words_dictionary(
    callback: types.CallbackQuery, bot: Bot, state: FSMContext
):
    language = callback.data.split("_")[-1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    user = users.find_one({"user_id": user_id})
    words = user["dictionaries"][language]
    if words:
        # Ability to get into the delete handler
        await state.set_state(FSMDeleteWord.print)
        await state.update_data(code=language, words=words)
        await edit_message(
            bot=bot,
            callback=callback,
            message="Choose how to display the dictionary",
            keyboard_fn=table_style_kb,
        )

    else:
        await edit_message(
            bot=bot,
            callback=callback,
            message="There are no words in this dictionary",
            keyboard_fn=partial(no_words_in_dict_kb, language),
        )


@router.callback_query(FSMDeleteWord.print, lambda message: message.data.startswith("print_words_"))
async def print_words(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    chat_id = callback.message.chat.id
    await state.set_state(FSMDeleteWord.number)
    data = await state.get_data()
    words, code = data["words"], data["code"]
    print_style = callback.data.split('_')[-1]
    # If the selected style is equal to the sketched word
    if print_style == 'word':
        text = ''
        for word in words:
            text += f'<tg-spoiler>{word["word"]}</tg-spoiler> - {word["translate"]}\n'
        await edit_message(
            bot=bot,
            callback=callback,
            keyboard_fn=back_to_dict_kb,
            message=f'{text}\n\nTo delete a word, write it',
        )
    # If the selected style is equal to the sketched translate
    elif print_style == 'translate':
        text = ''
        for word in words:
            text += f'{word["word"]} - <tg-spoiler>{word["translate"]}</tg-spoiler>\n'
        await edit_message(
            bot=bot,
            callback=callback,
            keyboard_fn=back_to_dict_kb,
            message=f'{text}\n\nTo delete a word, write it',
        )
    # If style is equal to normal word table
    elif print_style == 'plain':
        table = [[item["word"], item["translate"]] for item in words]
        await edit_message(
            bot=bot,
            callback=callback,
            keyboard_fn=back_to_dict_kb,
            message=f'<pre>{tabulate(table, headers=["word", "translation"], showindex=True, tablefmt="presto")}</pre>\n\nTo delete a word, write it',
        )


@router.message(FSMDeleteWord.number)
async def delete_word(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    data = await state.get_data()
    words, word, code = data["words"], message.text, data["code"]
    word_to_delete = None
    for elem in words:
        if word == elem["word"]:
            word_to_delete = elem
            break
    if word_to_delete:
        words.remove(word_to_delete)
        users.update_one(
            {"user_id": user_id},
            {"$pull": {f"dictionaries.{code}": word_to_delete}},
        )
        await state.clear()
        if words:
            table = [[item["word"], item["translate"]] for item in words]

            await message.answer(
                reply_markup=back_to_dict_kb(),
                parse_mode="HTML",
                text=f'<pre>{tabulate(table, headers=["word", "translation"], showindex=True, tablefmt="presto")}</pre>\n\nTo delete a word, write it',
            )
        else:
            await message.answer(
                text="There are no words in this dictionary",
                reply_markup=no_words_in_dict_kb(code),
            )
    else:
        await message.answer(text="❌ Wrong word ❌")
