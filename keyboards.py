from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb = [
   [KeyboardButton(text='🔍 ПО НАЗВАНИЮ')]
]
menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)

inline_buttons = [
  [InlineKeyboardButton(text="Следующий фильм", callback_data="next_movie")],
  [InlineKeyboardButton(text="Остановить", callback_data="stop")]
]
ikb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)