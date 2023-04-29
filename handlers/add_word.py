import asyncio
from aiogram import Bot, Router, types
from aiogram.filters.text import Text
from helpers import edit_message
from functools import partial
from keyboards.add_keyboard import add_action_kb


router = Router()


@router.callback_query(Text('add_word'))
async def add_word(callback: types.CallbackQuery, bot: Bot):
    languages = (
        {
            'value': 'RU',
            'label': 'Russian 🇷🇺'
        },
        {
            'value': 'SP',
            'label': 'Spanish 🇪🇸'
        },
    )
    await edit_message(callback=callback, bot=bot, message='Choose a language ',
                       keyboard_fn=partial(add_action_kb, languages=languages))

    await callback.answer('ok!')


@router.callback_query(lambda message: message.data.startswith('choose_language'))
async def choose_language(callback: types.CallbackQuery, bot: Bot):
    data = callback.data
    language_id = data.split('_')[-1]
    await callback.answer(language_id)
