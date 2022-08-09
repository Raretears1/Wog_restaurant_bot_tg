from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but_load = KeyboardButton('/Завантажити')
but_delete = KeyboardButton('/Видалити')

but_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(but_load).add(but_delete)