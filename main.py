import asyncio
import os
from aiogram import Bot, Dispatcher, Router, types
from get_news import news_rus_eng, send_news_ai_rus_eng
from content_main_channel import generate_interesting_fact, generate_market_analysis, weekly_summary, main_post
from config import OPENAI_API_KEY, CHANNEL_ID, API_TOKEN
import logging
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

ADMIN_ID = 947159905

router = Router()
# Логирование ошибок
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Создание диспетчера
dp = Dispatcher()

NEWS_FILE_PATH = 'weekly_news.txt'


def save_news_to_file(russian_news, english_news):
    with open(NEWS_FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(f"RUS: {russian_news}\n")
        file.write(f"ENG: {english_news}\n\n")


# Функция для чтения сохраненных новостей из файла
def load_news_from_file():
    if os.path.exists(NEWS_FILE_PATH):
        with open(NEWS_FILE_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    return ''


# Функция для очистки файла с новостями (после отправки обобщения)
def clear_news_file():
    with open(NEWS_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('')


# Функция для отправки новостей по расписанию
async def scheduled_news_sender():
    while True:
        try:
            now = datetime.now()
            if now.hour == 10 and now.minute == 0:
                russian_news, english_news = await news_rus_eng()
                if russian_news and english_news:
                    # Сохраняем новость в файл
                    save_news_to_file(russian_news, english_news)

                    # Отправляем ежедневные новости
                    await send_news_ai_rus_eng()
                    await main_post()

            # Если пятница (weekday == 4), в 12:00 отправляем обобщение новостей
            if now.weekday() == 4 and now.hour == 12 and now.minute == 0:
                # Читаем все новости из файла
                weekly_news_data = load_news_from_file()
                if weekly_news_data:
                    # Отправляем обобщение
                    await weekly_summary(weekly_news_data)
                    # Очищаем файл после отправки
                    clear_news_file()

            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error fetching or sending news: {e}")


MAX_POSTS_PER_DAY = 3

# Временные ограничения
START_HOUR = 6
END_HOUR = 16

# async def schedule_content_generation():
#     posts_today = 0
#     next_post_time = None
#
#     while True:
#         now = datetime.now()
#
#         # Сбросить счетчик постов и `next_post_time` в начале нового дня
#         if now.hour == 0 and now.minute == 0:
#             posts_today = 0
#             next_post_time = None
#
#         # Проверяем, если лимит постов не достигнут и время для следующего поста подошло
#         if posts_today < MAX_POSTS_PER_DAY and (next_post_time is None or now >= next_post_time):
#             # Устанавливаем случайное время для следующего поста
#             next_post_hour = random.randint(START_HOUR, END_HOUR)
#             next_post_minute = random.randint(0, 59)
#             next_post_time = now.replace(hour=next_post_hour, minute=next_post_minute, second=0, microsecond=0)
#
#             # Если время уже прошло, устанавливаем следующий день
#             if next_post_time < now:
#                 next_post_time += timedelta(days=1)
#
#         # Если текущее время >= времени для следующего поста, публикуем контент
#         if next_post_time is not None and now >= next_post_time:
#             content_type = random.choice([generate_market_analysis, generate_interesting_fact])
#             await content_type()  # Публикуем выбранный контент
#
#             posts_today += 1  # Увеличиваем счетчик постов
#             next_post_time = None  # Сброс времени следующего поста
#
#         # Проверка каждые 60 секунд
#         await asyncio.sleep(60)

# Инлайн-кнопки для панели администратора
admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вывести главное меню", callback_data="main_menu")],
        [InlineKeyboardButton(text="📊 Разместить аналитику", callback_data="post_analysis")],
        [InlineKeyboardButton(text="🌾 Вывести интересный факт", callback_data="post_fact")]
    ]
)


@router.message(Command("admin"))
async def show_admin_panel(message: types.Message):
    # Проверяем, является ли отправитель администратором
    if message.from_user.id == ADMIN_ID:
        await message.answer("Выберите действие:", reply_markup=admin_keyboard)
    else:
        await message.answer("У вас нет доступа к этой команде.")


# Обработчик нажатий на кнопки
@router.callback_query(lambda c: c.data in ["post_analysis", "post_fact", 'main_menu'])
async def handle_admin_buttons(callback_query: CallbackQuery):
    action = callback_query.data
    if action == "post_analysis":
        await generate_market_analysis()
    elif action == "post_fact":
        await generate_interesting_fact()
    elif action == "main_menu":
        await main_post()

    # Уведомляем администратора об отправке данных
    await callback_query.answer("Информация успешно отправлена в канал!")


async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)  # Подключаем маршрутизацию команд
    # Запускаем задачу для отправки новостей
    asyncio.create_task(scheduled_news_sender())
    # asyncio.create_task(schedule_content_generation())


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
