import asyncio

import openai
from config import OPENAI_API_KEY, CHANNEL_ID, API_TOKEN
from parsers import oilworld_parser, prozerno_parser, zol_parser, agroinvestor_parser, aemcx_parser, agroinvestor, \
    tg_channel, format_news, oleoscope, agrotrend_parse, interfaks_parse, agroxxi_parse  # Импортируй остальные парсеры
from price import final_output, txt_chicago, txt_moex, txt_matif
# from selenium_parsers import collect_articles_text  # Импортируй функции для работы с Selenium
from aiogram import Bot
import datetime

openai.api_key = OPENAI_API_KEY
bot = Bot(token=API_TOKEN)


def converted_file(url):
    with open(url, 'r', encoding='utf-8') as file:
        return file.read()


def news_archive(url, text, date):
    with open(url, 'w', encoding='utf-8') as file:
        file.write(f'{date},\n, {text}')


# async def fetch_news():
#     oilworld_news = oilworld_parser('https://www.oilworld.ru/')
#     zol_news = zol_parser('https://www.zol.ru/')
#     prozerno_news = prozerno_parser('https://prozerno.ru/')
#     investing_news = agroinvestor_parser('https://www.agroinvestor.ru/')
#     oleoscope_news = oleoscope('https://oleoscope.com/news/')
#     agrotrend_news = agrotrend_parse('https://agrotrend.ru/?s=Зерно')
#     interfaks_news = interfaks_parse('https://www.interfax.ru/business/')
#     agroxxi_news = agroxxi_parse('https://www.agroxxi.ru/mirovye-agronovosti')
#     formatted_agroxxi_news = format_news('Источник: https://www.agroxxi.ru', agroxxi_news)
#     # aemcx_news = aemcx_parser('https://www.aemcx.com/')
#     formatted_oilworld_news = format_news('Источник: https://www.oilworld.ru', oilworld_news)
#     formatted_zol_news = format_news('Источник: https://www.zol.ru', zol_news)
#     formatted_prozerno_news = format_news('Источник: https://prozerno.ru', prozerno_news)
#     formatted_investing_news = format_news('Источник: https://www.agroinvestor.ru', investing_news)
#     formatted_oleoscope_news = format_news('Источник: https://oleoscope.com', oleoscope_news)
#     formatted_agrotrend_news = format_news('Источник: https://agrotrend.ru', agrotrend_news)
#     formatted_interfax_news = format_news('Источник: https://www.interfax.ru', interfaks_news)
#     # formatted_aemcx_news = format_news('Источник: AEMCX', aemcx)
#     formatted_tg_channel = tg_channel()
#     prompt = (
#         f"Новости с сайтов: \n{formatted_agroxxi_news}\n{formatted_zol_news}\n{formatted_prozerno_news}\n{formatted_investing_news}\n{formatted_tg_channel}\n{formatted_oilworld_news}\n{formatted_oleoscope_news}\n{formatted_agrotrend_news}\n{formatted_interfax_news}")  #
#     news_archive('news_archive.txt', prompt, datetime.datetime.now())
#     file = converted_file(r'example.txt')
#     try:
#         response = await openai.ChatCompletion.acreate(
#             model='gpt-4o-mini',
#             messages=[
#                 {"role": "system", "content":  f'''Собери и обобщи ключевые новости на русском языке, выделяя значимые события по указанным темам. Подай информацию живо и увлекательно. Структура и оформление:
#
# 1. **Тон и стиль**:
#    - Текст должен быть легким для восприятия, но при этом информативным.
#    - Сделай текст разнообразным по стилю, добавляй эмодзи для живости.
#    - Каждую новость пиши отрывком и размещай ссылки на источники под каждой новостью.
#    - Подавай новость в контексте страны, где происходит событие, и избегай дублирования.
#
# 2. **Темы новостей**:
#    Используй следующие темы для поиска и создания новостей:
#    GASC, TMO, TCP, OC, MIT, SAGO, GTC, OAIC, DGF, ODC, SLAL, OFAC, BRICS, CBOP, MATIF, AgRurual, strategie grains, safras & Mercado, intertek, amspec, пальмовое масло, посев, кукуруза, пшеница, соя, оценка производства, ячмень, прогноз урожая, usda отчет, задержка грузов, WHFOB, CRFOB, BRFOB, LCO, brent, ZS, соевые бобы, ZC, кукуруза, ZW, agritel, deepwater, shallowwater, FOB, CIF, Incoterms, GAFTA, FOSFA, SBPP, SFCO, SFMP, DDGS, pulses, WASDE, Report, Rabobank, Балтийский индекс, Индекс Panamax, S&P Global Commodity Insights, Abiove, Weekly Soybean Complex, IGC, oilworld.ru, FREE ON-BOARD BLACK SEA PORTS, SUNFLOWER OIL EXPORT, SUNFLOWER MEAL EXPORT, PRICE SUNFLOWER OIL U.S. DOLLAR METRIC TON, PALM OIL MALASYA CRUDE 1, NASDAQ (биржа) Commodity Index Bean Oil Excess Return, SOYBEAN OIL FUTURES FRONT-MONTH CONTRACT.
#
# 3. **Пример формата новостей**:
#    {file}
#
# 4. **Обобщение**:
#    Добавь в конце всей информации краткий итог по ключевым тенденциям и прогнозам, выявленным в новостях.
#    '''
#
#                  },
#                 {"role": "user", "content": prompt},
#             ],
#             max_tokens=10000
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         print(f"Ошибка OpenAI API: {e}")
#         return None
#
#
# # Функция для отправки сообщений в канал Telegram
# async def send_news_to_channel(news):
#     if news:
#         await bot.send_message(CHANNEL_ID, f'''AGROCOR INFORMS 🌾\n\n{final_output}\n{txt}\n\n{news}\n\n🤝OFFERS ➡➡➡ https://t.me/+F8OsiZiNLg00NTY6\n🚢 VESSEL CATCHER ➡➡➡ https://t.me/+AqsaM2xqhS44NDQy\n🔥💰 TRADER’S STORIES ➡➡➡ https://t.me/+bzwCOPgtSWMyNTQ
# ''', disable_web_page_preview=True)
#     else:
#         await bot.send_message(CHANNEL_ID, "Не удалось получить новости на данный момент.")
#

async def news_rus_eng():
    file = converted_file(r'example.txt')
    txt = f'''Собери и обобщи ключевые новости на русском языке, выделяя значимые события по указанным темам. Подай информацию живо и увлекательно. Структура и оформление:

    1. **Тон и стиль**:
       - Текст должен быть легким для восприятия, но при этом информативным.
       - Сделай текст разнообразным по стилю, добавляй эмодзи для живости.
       - Каждую новость пиши отрывком и размещай ссылки на источники под каждой новостью.
       - Подавай новость в контексте страны, где происходит событие, и избегай дублирования.
       - Ограничь общий текст до 4000 символов.

    2. **Темы новостей**:
       Используй следующие темы для поиска и создания новостей:
       GASC, TMO, TCP, OC, MIT, SAGO, GTC, OAIC, DGF, ODC, SLAL, OFAC, BRICS, CBOP, MATIF, AgRurual, strategie grains, safras & Mercado, intertek, amspec, пальмовое масло, посев, кукуруза, пшеница, соя, оценка производства, ячмень, прогноз урожая, usda отчет, задержка грузов, WHFOB, CRFOB, BRFOB, LCO, brent, ZS, соевые бобы, ZC, кукуруза, ZW, agritel, deepwater, shallowwater, FOB, CIF, Incoterms, GAFTA, FOSFA, SBPP, SFCO, SFMP, DDGS, pulses, WASDE, Report, Rabobank, Балтийский индекс, Индекс Panamax, S&P Global Commodity Insights, Abiove, Weekly Soybean Complex, IGC, oilworld.ru, FREE ON-BOARD BLACK SEA PORTS, SUNFLOWER OIL EXPORT, SUNFLOWER MEAL EXPORT, PRICE SUNFLOWER OIL U.S. DOLLAR METRIC TON, PALM OIL MALASYA CRUDE 1, NASDAQ (биржа) Commodity Index Bean Oil Excess Return, SOYBEAN OIL FUTURES FRONT-MONTH CONTRACT.

    3. **Пример формата новостей**:
       {file}

    4. **Обобщение**:
       Добавь в конце всей информации краткий итог по ключевым тенденциям и прогнозам, выявленным в новостях.
       '''

    try:
        response = await openai.ChatCompletion.acreate(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": txt},
                {"role": "user", "content": txt},
            ],
            max_tokens=3000  # Ограничиваем токены, чтобы снизить вероятность превышения 4000 символов
        )
        russian_news = response['choices'][0]['message']['content'].strip()

        # Убедимся, что текст не превышает 4000 символов
        if len(russian_news) > 4000:
            russian_news = russian_news[:4000]

        # Перевод на английский
        translation_prompt = f"Please translate the following text to English:\n\n{russian_news}"
        translation_response = await openai.ChatCompletion.acreate(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Translate the news text to English."},
                {"role": "user", "content": translation_prompt},
            ],
            max_tokens=3000
        )
        english_news = translation_response['choices'][0]['message']['content'].strip()

        # Убедимся, что текст на английском также не превышает 4000 символов
        if len(english_news) > 4000:
            english_news = english_news[:4000]

        return russian_news, english_news

    except Exception as e:
        print(f"Ошибка OpenAI API: {e}")
        return None, None


# Функция для отправки сообщений в канал Telegram
async def send_news_ai_rus_eng():
    russian_news, english_news = await news_rus_eng()

    if russian_news and english_news:
        # Отправляем новости на русском
        await bot.send_message(CHANNEL_ID, f'''AGROCOR INFORMS 🌾\nRUS\n\n{final_output}\n{txt_moex}\n{txt_chicago}\n{txt_matif}\n\n{russian_news}\n\n🤝OFFERS ➡➡➡ https://t.me/+F8OsiZiNLg00NTY6\n🚢 VESSEL CATCHER ➡➡➡ https://t.me/+AqsaM2xqhS44NDQy\n🔥💰 TRADER’S STORIES ➡➡➡ https://t.me/+bzwCOPgtSWMyNTQ
        ''', disable_web_page_preview=True)

        # Отправляем новости на английском
        await bot.send_message(CHANNEL_ID, f'''AGROCOR INFORMS 🌾\nENG\n\n{final_output}\n{txt_moex}\n{txt_chicago}\n{txt_matif}\n\n{english_news}\n\n🤝OFFERS ➡➡➡ https://t.me/+F8OsiZiNLg00NTY6\n🚢 VESSEL CATCHER ➡➡➡ https://t.me/+AqsaM2xqhS44NDQy\n🔥💰 TRADER’S STORIES ➡➡➡ https://t.me/+bzwCOPgtSWMyNTQ
        ''', disable_web_page_preview=True)
    else:
        await bot.send_message(CHANNEL_ID, "Не удалось получить новости на данный момент.")


