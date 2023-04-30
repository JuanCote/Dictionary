from datetime import datetime
from aiogram import Bot, Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

from helpers import edit_message
from keyboards.main_keyboard import main_kb
from mongo_db import users

router = Router()

MAIN_TEXT = "Hello 👋\nThis is custom dictionary bot 📖"


@router.message(Command("start"))
async def start(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    user_in_db = users.find_one({"user_id": user_id})
    if not user_in_db:
        users.insert_one({"user_id": user_id, "dictionary": []})
    await message.answer(text=MAIN_TEXT, reply_markup=main_kb())


@router.callback_query(Text("back_to_main"))
async def back_to_main(callback: types.CallbackQuery, bot: Bot):
    await edit_message(
        callback=callback, bot=bot, keyboard_fn=main_kb, message=MAIN_TEXT
    )
