from aiogram.utils import executor

import handlers
from create_bot import dp

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)