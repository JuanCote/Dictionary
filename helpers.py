from aiogram import Bot, types


async def edit_message(bot: Bot, message: str,
                       callback: types.CallbackQuery, keyboard_fn):
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id
    return await bot.edit_message_text(reply_markup=keyboard_fn(),
                                       message_id=message_id, text=message,
                                       chat_id=chat_id)
