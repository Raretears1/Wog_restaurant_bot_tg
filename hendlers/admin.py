from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State  , StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_dp
from key_boards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    compound = State()
    price = State()


# Перевіряємо ID юзера для адмінки, чи він є адміном телеграм групи, якщо так то він може реєструвати меню, якщо ні то ні

# dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Добрий день, можете господарювати",
                           reply_markup=admin_kb.but_case_admin)
    await message.delete()


# Початок нового пункта в меню
# @dp.message_handler(commands='Завантажити', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Завантаж фото')


# Скасувати ввод
# @dp.message_handler(state="*", commands='скасувати')
# @dp.message_handler(Text(equals='скасувати', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OKEY!")


# Перша відповідь та запис її до словаря
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Тепер вводи назву')


# Друга відповідь
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Тепер вводи склад інгрідієнтів')


# Третя відповідь
# @dp.message_handler(state=FSMAdmin.compound)
async def load_compound(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['compound'] = message.text
        await FSMAdmin.next()
        await message.reply('Тепер введіть ціну')


# Четверта відповідь та записуємо дані
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text

        await sqlite_dp.sql_add_command(state)

        await state.finish()


# @dp.callback_query_handlers(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_dp.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} видалено.', show_alert=True)


# @dp.message_handler(commands='Видалити')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_dp.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nСклад: {ret[2]}\n Ціна: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Видалити {ret[1]}', callback_data=f'del {ret[1]}')))


# Реєструємо хендлерси

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Завантажити'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_compound, state=FSMAdmin.compound)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='скасувати')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, state="*", commands='Видалити')

