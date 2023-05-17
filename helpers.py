from aiogram import Bot, types

from mongo_db import users


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


languages_codes = {
    "🇨🇳": {"ZH": "Китайский (中文)"},
    "🇯🇵": {"JP": "Японский (日本語)"},
    "🇺🇸": {"EN": "Английский (English)"},
    "🇪🇸": {"ES": "Испанский (Español)"},
    "🇫🇷": {"FR": "Французский (Français)"},
    "🇩🇪": {"DE": "Немецкий (Deutsch)"},
    "🇮🇹": {"IT": "Итальянский (Italiano)"},
    "🇷🇺": {"RU": "Русский (Русский)"},
    "🇵🇹": {"PT": "Португальский (Português)"},
    "🇰🇷": {"KO": "Корейский (한국어)"},
    "🇳🇱": {"NL": "Голландский (Nederlands)"},
    "🇸🇪": {"SV": "Шведский (Svenska)"},
    "🇳🇴": {"NO": "Норвежский (Norsk)"},
    "🇩🇰": {"DA": "Датский (Dansk)"},
    "🇵🇱": {"PL": "Польский (Polski)"},
    "🇹🇷": {"TR": "Турецкий (Türkçe)"},
    "🇮🇩": {"ID": "Индонезийский (Bahasa Indonesia)"},
    "🇻🇳": {"VI": "Вьетнамский (Tiếng Việt)"},
    "🇨🇿": {"CS": "Чешский (Čeština)"},
    "🇬🇷": {"EL": "Греческий (Ελληνικά)"},
    "🇮🇳": {"HI": "Хинди (हिन्दी)"},
    "🇫🇮": {"FI": "Финский (Suomi)"},
    "🇮🇱": {"HE": "Иврит (עברית)"},
    "🇷🇸": {"SR": "Сербский (Српски)"},
    "🇷🇴": {"RO": "Румынский (Română)"},
    "🇭🇺": {"HU": "Венгерский (Magyar)"},
    "🇸🇦": {"AR": "Арабский (العربية)"},
    "🇹🇭": {"TH": "Тайский (ภาษาไทย)"},
    "🇿🇦": {"AF": "Африкаанс (Afrikaans)"},
    "🇵🇭": {"TL": "Филиппинский (Tagalog)"},
    "🇧🇬": {"BG": "Болгарский (Български)"},
    "🇭🇷": {"HR": "Хорватский (Hrvatski)"},
}
