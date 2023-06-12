
from aiogram import Bot, types
from translate import Translator

from mongo_db import users


def translate_word(to_lang, word):
    translator = Translator(from_lang='en', to_lang=to_lang)
    return translator.translate(word).lower()


def make_center_word(total_length, word):
    padding_length = total_length - len(word)
    left_padding = padding_length // 2
    print(left_padding, word)
    right_padding = padding_length - left_padding + 1
    centered_word = " " * left_padding + word + " " * right_padding
    return centered_word


def make_dict_row(first_word, second_word, room_for_one_word, dash_count):
    first_centered_word = make_center_word(room_for_one_word, first_word.lower())
    second_centered_word = make_center_word(room_for_one_word, second_word.lower())
    return f"{'-' * dash_count}\n|{first_centered_word}|{second_centered_word}|\n"


async def edit_message(
    bot: Bot,
    message: str,
    callback: types.CallbackQuery,
    keyboard_fn=None,
    parse_mode="HTML",
):
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id
    return await bot.edit_message_text(
        reply_markup=keyboard_fn() if keyboard_fn is not None else None,
        message_id=message_id,
        text=message,
        chat_id=chat_id,
        parse_mode=parse_mode,
    )


def get_dictionaries(user_id):
    user = users.find_one({"user_id": user_id})
    if not user["dictionaries"]:
        return []
    else:
        dictionaries = list()
        for dictionary in user["dictionaries"].keys():
            for elem in languages_codes:
                if dictionary in languages_codes[elem]:
                    dictionaries.append(
                        {
                            "code": dictionary,
                            "label": languages_codes[elem][dictionary],
                        }
                    )
        return dictionaries


def delete_dictionary_from_db(user_id: int, dict_code: str):
    return users.update_one(
        {"user_id": user_id},
        {"$unset": {f"dictionaries.{dict_code}": ""}},
    )


def get_dict_label_by_code(dict_code: str):
    for elem in languages_codes:
        if dict_code in languages_codes[elem]:
            return languages_codes[elem][dict_code]


languages_codes = {
    "🇨🇳": {"ZH": "中文"},
    "🇯🇵": {"JP": "日本語"},
    "🇺🇸": {"EN": "English"},
    "🇪🇸": {"ES": "Español"},
    "🇫🇷": {"FR": "Français"},
    "🇩🇪": {"DE": "Deutsch"},
    "🇮🇹": {"IT": "Italiano"},
    "🇷🇺": {"RU": "Русский"},
    "🇵🇹": {"PT": "Português"},
    "🇰🇷": {"KO": "한국어"},
    "🇳🇱": {"NL": "Nederlands"},
    "🇸🇪": {"SV": "Svenska"},
    "🇳🇴": {"NO": "Norsk"},
    "🇩🇰": {"DA": "Dansk"},
    "🇵🇱": {"PL": "Polski"},
    "🇹🇷": {"TR": "Türkçe"},
    "🇮🇩": {"ID": "Bahasa Indonesia"},
    "🇻🇳": {"VI": "Tiếng Việt"},
    "🇨🇿": {"CS": "Čeština"},
    "🇬🇷": {"EL": "Ελληνικά"},
    "🇮🇳": {"HI": "हिन्दी"},
    "🇫🇮": {"FI": "Suomi"},
    "🇮🇱": {"HE": "עברית"},
    "🇷🇸": {"SR": "Српски"},
    "🇷🇴": {"RO": "Română"},
    "🇭🇺": {"HU": "Magyar"},
    "🇸🇦": {"AR": "العربية"},
    "🇹🇭": {"TH": "ภาษาไทย"},
    "🇿🇦": {"AF": "Afrikaans"},
    "🇵🇭": {"TL": "Tagalog"},
    "🇧🇬": {"BG": "Български"},
    "🇭🇷": {"HR": "Hrvatski"},
}
