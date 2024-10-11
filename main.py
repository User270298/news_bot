import asyncio
from aiogram import Bot, Dispatcher
from get_news import fetch_news, send_news_to_channel
from config import OPENAI_API_KEY, CHANNEL_ID, API_TOKEN
import logging
from datetime import datetime

# Логирование ошибок
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Создание диспетчера
dp = Dispatcher()


async def scheduled_news_sender():
    while True:
        try:
            now = datetime.now()
            if now.hour in [7] and now.minute == 0:
                news = await fetch_news()
                await send_news_to_channel(news)
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error fetching or sending news: {e}")



async def on_startup(dp):
    # Запускаем задачу для отправки новостей
    asyncio.create_task(scheduled_news_sender())


async def main():
    # Включаем бота в контекст диспетчера
    dp["bot"] = bot

    # Добавляем запуск задачи при старте
    await on_startup(dp)

    # Запускаем опрос
    await dp.start_polling(bot)


async def run_bot_with_restart():
    while True:
        try:
            await main()  # Запуск основной программы
        except Exception as e:
            logging.error(f"Bot encountered an error: {e}")
            await asyncio.sleep(10)  # Ожидание перед перезапуском


if __name__ == '__main__':
    asyncio.run(run_bot_with_restart())