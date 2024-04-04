import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.filters import CommandStart
from config_reader import config
from keyboards import menu, ikb
import sys
sys.path.append("D:\Рабочий стол\kursovaya\model")
from model.recommendation import get_recommendations

#@movie_recomm_bot

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


def get_movies(user_title):
    recommended_movies = get_recommendations(user_title)
    return recommended_movies


@dp.message(CommandStart())
async def start_send(message: types.Message):
  await message.answer('Привет👋\nЯ помогу тебе найти интересные фильмы на основе твоих предпочтений и настроений ;)',
                       reply_markup=menu)


movies = []
movies2 = []

@dp.message(lambda message: message.text == '🔍 ПО НАЗВАНИЮ')
async def search_name_button(message: types.Message):
    await message.answer('Введи название фильма')    
    
    # Получение названия фильма от пользователя
    @dp.message()
    async def get_title(message: types.Message):
        global movies, movies2
        title = message.text
        movies = get_movies(title)
        movies2 = movies.copy()
        await message.answer('\n'.join(movies))
        
        # Отправляем первый фильм с клавиатурой
        if movies:
            await send_movie_with_buttons(message, movies, 0, ikb)


@dp.callback_query(lambda query: query.data == 'next_movie')
async def next_movie_callback(query: types.CallbackQuery):
        index = movies2.index(query.message.text) + 1 # Получаем индекс следующего фильма из данных пользователя
        new_movies_list = movies[index:]  # Получаем список фильмов из сообщения
        await send_movie_with_buttons(query.message, new_movies_list, index, query.message.reply_markup)


async def send_movie_with_buttons(message, movies, index, keyboard):
    global movies2
    if index < len(movies2):
        await message.answer(f"{movies2[index]}", reply_markup=keyboard)
    else:
        await message.answer("Упс, фильмы закончились")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())