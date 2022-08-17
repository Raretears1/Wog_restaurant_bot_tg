from aiogram import types, Dispatcher
from create_bot import dp, bot
from key_boards import kb_client
from data_base import sqlite_dp


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "СМАЧНОГО!", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply(
            'Спілкування з ботом через ЛС, звертайтесь до нього :\nhttps://t.me/WOK_noodles_and_rice_bot'
        )


# @dp.message_handler(commands=['Режим_роботи'])
async def when_open(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Понеділок - Четверг з 09:00 до 20:00 \nП'ятниця - Суббота з 11:00 до 19:00 ")


# @dp.message_handler(commands=['Де_ми_?'])
async def where_open(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "метро Лук'янівка, вул.Татарська 10")


# @dp.message_handler(commands=['/Меню'])
async def wok_menu_command(message: types.Message):
    await sqlite_dp.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(when_open, commands=['Режим_роботи'])
    dp.register_message_handler(where_open, commands=['Де_ми_?'])
    dp.register_message_handler(wok_menu_command, commands=['/Меню'])