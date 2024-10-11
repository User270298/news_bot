import openai
from config import OPENAI_API_KEY, CHANNEL_ID, API_TOKEN
from parsers import oilworld_parser, prozerno_parser, zol_parser, agroinvestor_parser, aemcx_parser, agroinvestor, \
    tg_channel, format_news, oleoscope, agrotrend_parse, interfaks_parse, agroxxi_parse  # Импортируй остальные парсеры
from price import final_output, txt
# from selenium_parsers import collect_articles_text  # Импортируй функции для работы с Selenium
from aiogram import Bot
import datetime

openai.api_key = OPENAI_API_KEY
bot = Bot(token=API_TOKEN)


def converted_file(url):
    with open(url, 'r', encoding='utf-8') as file:
        return file.read()


def news_archive(url, text, date):
    with open(url, 'a', encoding='utf-8') as file:
        file.write(f'{date},\n, {text}')


async def fetch_news():
    oilworld_news = oilworld_parser('https://www.oilworld.ru/')
    zol_news = zol_parser('https://www.zol.ru/')
    prozerno_news = prozerno_parser('https://prozerno.ru/')
    investing_news = agroinvestor_parser('https://www.agroinvestor.ru/')
    oleoscope_news = oleoscope('https://oleoscope.com/news/')
    agrotrend_news = agrotrend_parse('https://agrotrend.ru/?s=Зерно')
    interfaks_news = interfaks_parse('https://www.interfax.ru/business/')
    agroxxi_news = agroxxi_parse('https://www.agroxxi.ru/mirovye-agronovosti')
    formatted_agroxxi_news = format_news('Источник: https://www.agroxxi.ru', agroxxi_news)
    # aemcx_news = aemcx_parser('https://www.aemcx.com/')
    formatted_oilworld_news = format_news('Источник: https://www.oilworld.ru', oilworld_news)
    formatted_zol_news = format_news('Источник: https://www.zol.ru', zol_news)
    formatted_prozerno_news = format_news('Источник: https://prozerno.ru', prozerno_news)
    formatted_investing_news = format_news('Источник: https://www.agroinvestor.ru', investing_news)
    formatted_oleoscope_news = format_news('Источник: https://oleoscope.com', oleoscope_news)
    formatted_agrotrend_news = format_news('Источник: https://agrotrend.ru', agrotrend_news)
    formatted_interfax_news = format_news('Источник: https://www.interfax.ru', interfaks_news)
    # formatted_aemcx_news = format_news('Источник: AEMCX', aemcx)
    formatted_tg_channel = tg_channel()
    prompt = (
        f"Новости с сайтов: \n{formatted_agroxxi_news}\n{formatted_zol_news}\n{formatted_prozerno_news}\n{formatted_investing_news}\n{formatted_tg_channel}\n{formatted_oilworld_news}\n{formatted_oleoscope_news}\n{formatted_agrotrend_news}\n{formatted_interfax_news}")  #
    news_archive('news_archive.txt', prompt, datetime.datetime.now())
    file = converted_file(r'example.txt')
    try:
        response = await openai.ChatCompletion.acreate(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": f'''Ты должен суммировать ключевые моменты новостей на русском языке,
                                                 делая текст увлекательным и разнообразным по стилю.
                                                 Не добавляй заголовки, используй эмодзи, чтобы сделать
                                                 текст живее.
                                                 В новостях опирайся на следующие слова():
                                                 CBOP / MATIF / AgRurual/ strategie grains / safras & Mercado / intertek / amspec
                                                 и все в аспекте текстов на тему палсьмовое масло , посев , кукуруза ,
                                                 пшеница , соя, оценка производства , ячмень , прогноз урожая , usda отчет ,задержка грузов
                                                  Новости выводи разбивая по странам, в которых происходят события.
                                                  Текст выводи в формате согласно приведенных примеров ниже.
                                                  Пример форматов новостей:
                                                  {file}
                                                  Всегда добавляй обобщение в конце всей информации.
                                                  Источники в конце текста указывай в виде ссылок на сайты.'''
                 },
                {"role": "user", "content": prompt},
            ],
            max_tokens=10000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Ошибка OpenAI API: {e}")
        return None


# Функция для отправки сообщений в канал Telegram
async def send_news_to_channel(news):
    if news:
        await bot.send_message(CHANNEL_ID, f'''AGROCOR INFORMS 🌾\n\n{final_output}\n{txt}\n\n{news}\n\n🤝OFFERS ➡➡➡ https://t.me/+F8OsiZiNLg00NTY6\n🚢 VESSEL CATCHER ➡➡➡ https://t.me/+AqsaM2xqhS44NDQy\n🔥💰 TRADER’S STORIES ➡➡➡ https://t.me/+bzwCOPgtSWMyNTQ
''', disable_web_page_preview=True)
    else:
        await bot.send_message(CHANNEL_ID, "Не удалось получить новости на данный момент.")