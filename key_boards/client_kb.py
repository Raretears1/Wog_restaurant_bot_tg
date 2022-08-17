from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but1 = KeyboardButton('/Режим_роботи')
but2 = KeyboardButton('/Де_ми_?')
but3 = KeyboardButton('/Меню')
# but4 = KeyboardButton('Відправити номер', request_contact=True)
# but5 = KeyboardButton('Моє місцезнаходження', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(but3).row(but1, but2)
