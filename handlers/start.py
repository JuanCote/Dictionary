from aiogram import Bot, Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

from helpers import edit_message
from keyboards.main_keyboard import main_kb

router = Router()

MAIN_TEXT = "Hello 👋\nThis is custom dictionary bot 📖"


@router.message(Command("start"))
async def start(message: types.Message, bot: Bot):
    await message.answer(text=MAIN_TEXT, reply_markup=main_kb())


@router.callback_query(Text("back_to_main"))
async def back_to_main(callback: types.CallbackQuery, bot: Bot):
    await edit_message(
        callback=callback, bot=bot, keyboard_fn=main_kb, message=MAIN_TEXT
    )
