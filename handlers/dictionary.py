from functools import partial

from aiogram import Router, types, Bot
from aiogram.filters import Text
from aiogram.filters.callback_data import CallbackData

from handlers.add_word import languages
from handlers.start import MAIN_TEXT
from helpers import edit_message
from keyboards.dictionary_keyboard import choose_dict_kb
from keyboards.main_keyboard import main_kb
from mongo_db import users

router = Router()


@router.callback_query(Text("dictionary"))
async def choose_dictionary_language(callback: types.CallbackQuery, bot: Bot):
    await edit_message(
        bot=bot,
        callback=callback,
        message="📖 Choose dictionary language 👀",
        keyboard_fn=partial(choose_dict_kb, languages),
    )


@router.callback_query(lambda message: message.data.startswith("choose_dict"))
async def get_words_dictionary(callback: types.CallbackQuery, bot: Bot):
    language = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    try:
        user = users.find_one({"user_id": user_id})
        words = user["dictionary"]
        if words:
            result = ""
            for elem in words:
                if elem["language_to"] == language:
                    word = elem["word"]
                    translate = elem["translate"]
                    result += f"{word} - {translate}\n"
            if not result:
                await bot.send_message(
                    chat_id=chat_id, text="There are no words in this dictionary"
                )
            else:
                await bot.send_message(chat_id=chat_id, text=result)
        else:
            await bot.send_message(
                chat_id=chat_id, text="There are no words in this dictionary"
            )
    except:
        await bot.send_message(chat_id=chat_id, text="DB_ERROR", reply_markup=main_kb())
    await bot.send_message(chat_id=chat_id, text=MAIN_TEXT, reply_markup=main_kb())
