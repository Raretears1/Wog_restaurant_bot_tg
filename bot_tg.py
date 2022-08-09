from aiogram.utils import executor
from create_bot import dp
from hendlers import client, admin, other
from data_base import sqlite_dp


async def on_startup(_):
    print('Bot is online')
    sqlite_dp.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
