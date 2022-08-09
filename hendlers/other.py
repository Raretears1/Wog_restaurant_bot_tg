from aiogram import types, Dispatcher
import json, string


# @dp.message_handler()
async def control_filthy_language(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply("Блін, не матюхаться мені тут!")
        await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(control_filthy_language)
