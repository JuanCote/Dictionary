from functools import partial

from aiogram import Router, types, Bot
from aiogram.filters import Text

from handlers.start import MAIN_TEXT
from helpers import get_dictionaries, edit_message, delete_dictionary_from_db, languages_codes, get_dict_label_by_code
from keyboards.settings.check_delete_dict_keyboard import check_delete_dict_kb
from keyboards.settings.delete_dictionaries_keyboard import delete_dict_kb
from keyboards.settings.main_settings_keyboard import main_settings_kb

router = Router()


@router.callback_query(Text("settings"))
async def choose_dictionary_language(callback: types.CallbackQuery, bot: Bot):
    await edit_message(
        bot=bot,
        callback=callback,
        message="Settings Menu 🔧",
        keyboard_fn=main_settings_kb
    )


@router.callback_query(lambda message: message.data.startswith("dict_delete"))
async def delete_dictionary(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    dict_code = callback.data.split("_")[-1]
    """
    If you access the handler through the settings menu, the last word after '_' will be 'delete'.
    If you came from deleting a dictionary, it will be '{dictionary_code}'
    """
    if dict_code != 'delete':
        delete_dictionary_from_db(user_id, dict_code)
    dictionaries = get_dictionaries(user_id)
    text = "Choose dictionary to delete 🗑️"
    if not dictionaries:
        text = "You don't have any dictionaries 🤷‍♂️"
    await edit_message(
        bot=bot,
        callback=callback,
        message=text,
        keyboard_fn=partial(delete_dict_kb, dictionaries)
    )


@router.callback_query(lambda message: message.data.startswith("check_delete_dict_"))
async def delete_dictionary(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    dict_code = callback.data.split("_")[-1]
    dict_label = get_dict_label_by_code(dict_code)
    text = f"Are you sure you want to delete the {dict_label} dictionary ⁉️"
    await edit_message(
        bot=bot,
        callback=callback,
        message=text,
        keyboard_fn=partial(check_delete_dict_kb, dict_code)
    )