from config import OPENAI_API_KEY, API_TOKEN, CHANNEL_ID_MAIN
import openai
from aiogram import Bot
import logging
import os
from aiogram import Router
from price import get_telegram_subscribers
from aiogram import Bot, Dispatcher

openai.api_key = OPENAI_API_KEY
bot = Bot(token=API_TOKEN)
router = Router()
ADMIN_ID = 947159905

async def weekly_summary(weekly_news_queue):
    # Формируем запрос для OpenAI
    if weekly_news_queue:
        combined_news_rus = "\n".join([f"- {rus}" for rus, _ in weekly_news_queue])
        combined_news_eng = "\n".join([f"- {eng}" for _, eng in weekly_news_queue])

        # Отправляем запрос на OpenAI для русского обобщения
        try:
            response_rus = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Собери ключевые новости недели из следующего текста."},
                    {"role": "user", "content": combined_news_rus}
                ],
                max_tokens=3000
            )
            weekly_summary_rus = response_rus['choices'][0]['message']['content'].strip()
        except Exception as e:
            logging.error(f"Error with OpenAI API for Russian summary: {e}")
            weekly_summary_rus = "Не удалось получить обобщение на русском языке."
            await bot.send_message(ADMIN_ID, f'Ошибка: {e}')
        # Отправляем запрос на OpenAI для английского обобщения
        try:
            response_eng = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Summarize the key events from the following news in English."},
                    {"role": "user", "content": combined_news_eng}
                ],
                max_tokens=3000
            )
            weekly_summary_eng = response_eng['choices'][0]['message']['content'].strip()
        except Exception as e:
            logging.error(f"Error with OpenAI API for English summary: {e}")
            weekly_summary_eng = "Failed to get weekly summary in English."
            await bot.send_message(ADMIN_ID, f'Ошибка: {e}')
        # Отправляем итоговые обобщения в канал
        await bot.send_message(
            CHANNEL_ID_MAIN,
            f"AGROCOR WEEKLY NEWS🌾\nRUS\n\n{weekly_summary_rus}",
            disable_web_page_preview=True
        )
        await bot.send_message(
            CHANNEL_ID_MAIN,
            f"AGROCOR WEEKLY NEWS 🌾\nENG\n\n{weekly_summary_eng}",
            disable_web_page_preview=True
        )


async def generate_market_analysis():
    try:
        MARKET_ANALYSIS_PROMPT = '''Собери краткий рыночный анализ агросферы какой нибудь отдельной области, включая такие аспекты, как качество и состояние сельскохозяйственных культур,
                                    влияние погодных условий на урожай, обновления по сельскохозяйственным технологиям и технике, основные тренды в торговле и ценах
                                    на агрокультуры (зерновые, масличные, бобовые и т.д.), логистические вопросы, которые могут влиять на поставки, а также общие
                                    экономические факторы, которые могут оказать влияние на сельскохозяйственные рынки. Включи информацию о текущих запросах на рынке,
                                    а также возможные прогнозы и риски, связанные с предстоящими сезонами.
                                    Темы для поиска аналититки и анализа рынка:
                                     GASC, TMO, TCP, OC, MIT, SAGO, GTC, OAIC, DGF, ODC, SLAL, OFAC, BRICS, CBOP, MATIF, AgRurual, strategie grains, safras & Mercado, intertek, amspec, пальмовое масло, посев, кукуруза, пшеница, соя, оценка производства, ячмень, прогноз урожая, usda отчет, задержка грузов, WHFOB, CRFOB, BRFOB, LCO, brent, ZS, соевые бобы, ZC, кукуруза, ZW, agritel, deepwater, shallowwater, FOB, CIF, Incoterms, GAFTA, FOSFA, SBPP, SFCO, SFMP, DDGS, pulses, WASDE, Report, Rabobank, Балтийский индекс, Индекс Panamax, S&P Global Commodity Insights, Abiove, Weekly Soybean Complex, IGC, oilworld.ru, FREE ON-BOARD BLACK SEA PORTS, SUNFLOWER OIL EXPORT, SUNFLOWER MEAL EXPORT, PRICE SUNFLOWER OIL U.S. DOLLAR METRIC TON, PALM OIL MALASYA CRUDE 1, NASDAQ (биржа) Commodity Index Bean Oil Excess Return, SOYBEAN OIL FUTURES FRONT-MONTH CONTRACT, MARS, NOFI, MITS, FCPOc3, По сообщению агенства FryersOil world, Wheat France FOB, Wheat EU Black Sea FOB, Barley France FOB,Barley EU Black Sea, Corn Argentina FOB/
                                    Corn EU Black Sea FOB, Ameropa ,MFG, adm , vittera , CHS , cereal crop , dahra, C&F, NOFI, commodity whether group, S&D, StoneX,KFA,Buildcom, Cargill , Bunge, Dreyfus, Olam , Avere, Wheat flour import, wheat flour export, MITS,vegoils .
'''
        # Получение рыночной аналитики на русском языке
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": MARKET_ANALYSIS_PROMPT},
                {"role": "user", "content": MARKET_ANALYSIS_PROMPT}
            ],
            max_tokens=1000
        )
        analysis_text = response['choices'][0]['message']['content'].strip()
        if len(analysis_text) > 1500:
            analysis_text = analysis_text[:1500]
        # Перевод на английский язык
        translation_prompt = f"Please translate the following text to English:\n\n{analysis_text}"
        translation_response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the market analysis text to English."},
                {"role": "user", "content": translation_prompt}
            ],
            max_tokens=1000
        )
        analysis_text_eng = translation_response['choices'][0]['message']['content'].strip()
        if len(analysis_text_eng) > 1500:
            analysis_text_eng = analysis_text_eng[:1500]
        # Отправка сообщений на русском и английском языках
        await bot.send_message(CHANNEL_ID_MAIN,
                               f"📊 Рыночная аналитика (RUS):\n{analysis_text}\n\n📊 Market Analysis (ENG):\n{analysis_text_eng}",
                               disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(ADMIN_ID,f'Ошибка: {e}')


# 3. Функция для генерации интересных фактов об агросфере
async def generate_interesting_fact():
    try:
        INTERESTING_FACT_PROMPT = '''Расскажи краткий интересный факт о сельском хозяйстве, охватывающий различные аспекты агросферы. Факт может касаться истории сельского
                    хозяйства, уникальных качеств разных культур (например, устойчивость к погодным условиям, методы улучшения урожайности),
                    современных технологий в сельском хозяйстве (например, дроны для мониторинга полей, умные системы орошения, новые виды удобрений
                    и способы их применения). Также включи факты об изменениях климата и их влиянии на агропроизводство, логистику сельхозпродукции,
                    и роли сельского хозяйства в глобальной экономике. Факт может быть связан с необычными методами выращивания, влиянием на здоровье,
                    и инновационными способами использования сельскохозяйственных продуктов.
                    Темы для поиска интересной информации и интересных фактов:
                     GASC, TMO, TCP, OC, MIT, SAGO, GTC, OAIC, DGF, ODC, SLAL, OFAC, BRICS, CBOP, MATIF, AgRurual, strategie grains, safras & Mercado, intertek, amspec, пальмовое масло, посев, кукуруза, пшеница, соя, оценка производства, ячмень, прогноз урожая, usda отчет, задержка грузов, WHFOB, CRFOB, BRFOB, LCO, brent, ZS, соевые бобы, ZC, кукуруза, ZW, agritel, deepwater, shallowwater, FOB, CIF, Incoterms, GAFTA, FOSFA, SBPP, SFCO, SFMP, DDGS, pulses, WASDE, Report, Rabobank, Балтийский индекс, Индекс Panamax, S&P Global Commodity Insights, Abiove, Weekly Soybean Complex, IGC, oilworld.ru, FREE ON-BOARD BLACK SEA PORTS, SUNFLOWER OIL EXPORT, SUNFLOWER MEAL EXPORT, PRICE SUNFLOWER OIL U.S. DOLLAR METRIC TON, PALM OIL MALASYA CRUDE 1, NASDAQ (биржа) Commodity Index Bean Oil Excess Return, SOYBEAN OIL FUTURES FRONT-MONTH CONTRACT, MARS, NOFI, MITS, FCPOc3, По сообщению агенства FryersOil world, Wheat France FOB, Wheat EU Black Sea FOB, Barley France FOB,Barley EU Black Sea, Corn Argentina FOB/
                    Corn EU Black Sea FOB, Ameropa ,MFG, adm , vittera , CHS , cereal crop , dahra, C&F, NOFI, commodity whether group, S&D, StoneX,KFA,Buildcom, Cargill , Bunge, Dreyfus, Olam , Avere, Wheat flour import, wheat flour export, MITS,vegoils .
'''

        # Получение интересного факта на русском языке
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": INTERESTING_FACT_PROMPT},
                {"role": "user", "content": INTERESTING_FACT_PROMPT}
            ],
            max_tokens=1000
        )
        fact_text = response['choices'][0]['message']['content'].strip()
        if len(fact_text) > 1500:
            fact_text = fact_text[:1500]
        # Перевод на английский язык
        translation_prompt = f"Please translate the following text to English:\n\n{fact_text}"
        translation_response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the interesting fact text to English."},
                {"role": "user", "content": translation_prompt}
            ],
            max_tokens=1000
        )
        fact_text_eng = translation_response['choices'][0]['message']['content'].strip()
        if len(fact_text_eng) > 1500:
            fact_text_eng = fact_text_eng[:1500]
        # Отправка сообщений на русском и английском языках
        await bot.send_message(CHANNEL_ID_MAIN,
                               f"🌾 Интересный факт (RUS):\n{fact_text}\n\n🌾 Interesting Fact (ENG):\n{fact_text_eng}",
                               disable_web_page_preview=True)

    except Exception as e:
        await bot.send_message(ADMIN_ID,f'Ошибка: {e}')


async def main_post():
    await bot.send_message(CHANNEL_ID_MAIN, f'''
📊 Статистика нашего канала на сегодня 📊
👥 Подписчики:
На данный момент на нашем канале AGROCOR нас уже {get_telegram_subscribers()} подписчиков!

🔎 Активность за последние 7 дней:
📈 Новых подписчиков: 1000
📉 Отписавшихся: 17
👁 Просмотров в день: 9

Каналы и боты AGROCOR:

🤖 Ассистент бот: https://t.me/agrocorassistant_bot
🚢 Фрахт бот: https://t.me/agrocorfreightassistant_bot
🌍 Новости агросектора: https://t.me/agrocornews_channel
📬 Предложения: https://t.me/+Qo-k-cCWpb9hMGIy
📝 Запросы: https://t.me/+xFOPd8ApOjVmNmFi
👨 Бот для разговоров: https://t.me/agrocor_companion_bot

⚡️ Спасибо, что вы с нами!
Мы продолжаем развиваться и готовы делиться с вами самой актуальной и интересной информацией! 🌱 Поделитесь нашим каналом с друзьями, чтобы нас стало ещё больше!''')




