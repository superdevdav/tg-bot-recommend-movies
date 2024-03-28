import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.filters import CommandStart
from config_reader import config
from keyboards import menu
import sys
sys.path.append("D:\Рабочий стол\kursovaya\model")
from model.recommendation import get_recommendations

#@movie_recomm_bot

def send_movies(user_title):
    recommended_movies = get_recommendations(user_title)
    return recommended_movies

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(CommandStart())
async def start_send(message: types.Message):
  await message.answer('Привет👋\nЯ помогу тебе найти интересные фильмы на основе твоих предпочтений и настроений ;)',
                       reply_markup=menu)

@dp.message()
async def echo(message: types.Message):
    user_title = message.text  # Получаем текст сообщения пользователя
    movies = send_movies(user_title)  # Вызываем функцию send_movies с полученным названием фильма
    await message.answer(" ".join(movies))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())