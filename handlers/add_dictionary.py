from aiogram import Router, types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.start import MAIN_TEXT
from helpers import languages_codes
from keyboards.main_keyboard import main_kb
from mongo_db import users

router = Router()


class FSMDeleteWord(StatesGroup):
    flag = State()


@router.callback_query(Text("add_dictionary"))
async def add_dictionary(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(FSMDeleteWord.flag)
    chat_id = callback.message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text="Enter the language flag for which you want to add a dictionary",
    )


@router.message(FSMDeleteWord.flag)
async def flag(message: types.Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    flag = message.text
    user = users.find_one({"user_id": user_id})
    if not flag in languages_codes:
        await bot.send_message(
            chat_id=chat_id, text="There is no such flag in my list, please try again"
        )
    else:
        code = tuple(languages_codes[flag].keys())[0]
        if code in user["dictionaries"]:
            await bot.send_message(
                chat_id=chat_id, text="You already have such a dictionary"
            )
        else:
            await state.clear()
            users.update_one(
                {"user_id": user_id}, {"$set": {f"dictionaries.{code}": []}}
            )
            await message.answer(text="The dictionary was successfully created 🥳")
            await message.answer(text=MAIN_TEXT, reply_markup=main_kb())
