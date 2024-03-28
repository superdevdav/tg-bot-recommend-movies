from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = [
   [KeyboardButton(text='🔍 ПО НАЗВАНИЮ')]
]
menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)