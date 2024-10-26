import yfinance as yf
from bs4 import BeautifulSoup
import requests

# Тикеры для биткоина, валютных пар и нефти
tickers = {
    'Bitcoin': 'BTC-USD',
    'USD/RUB': 'USDRUB=X',
    'EUR/RUB': 'EURRUB=X',
    'Brent Crude Oil': 'BZ=F',
    'USD/CNY': 'CNY=X',
    'USD/TRY': 'TRY=X',
    'USD/EUR': 'EURUSD=X',
}

# Период для запроса данных (например, 5 дней)
period = "5d"


# Функция для получения цен
def get_prices():
    prices = {}

    for name, ticker in tickers.items():
        # Создаем объект тикера
        stock = yf.Ticker(ticker)

        # Получаем исторические данные
        data = stock.history(period=period)

        # Проверяем, что DataFrame не пустой и содержит хотя бы одну строку данных
        if not data.empty and len(data) > 0:
            # Получаем последнюю цену закрытия
            last_price = data['Close'].iloc[-1]
            # Округляем значение и добавляем в словарь
            if name == 'Bitcoin':
                prices['btc_price'] = round(last_price, 1)
            elif name == 'Brent Crude Oil':
                prices['oil_price'] = round(last_price, 2)
            else:
                # Добавляем другие валюты
                prices[name.lower().replace('/', '_')] = round(last_price, 4)
        else:
            prices[name] = None  # Если данных нет, присваиваем None

    return prices


# Вызов функции для получения цен


# Функция для получения цен на агрокультуры с бирж CME и MATIF
def get_cme_matif_prices():
    # CME (Чикагская биржа)
    cme_tickers = {
        'Пшеница': 'ZW=F',
        'Кукуруза': 'ZC=F',
        'Соевые бобы': 'ZS=F',
    }
    # Переменные для хранения результатов
    cme_output = "CHICAGO - "
    # Получение данных для CME
    for name, ticker in cme_tickers.items():
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            last_price = data['Close'].iloc[-1]
            # Добавляем данные в строку с запятой
            if name == "Пшеница":
                cme_output += f"{last_price:.2f}$ wheat🌾, "
            elif name == "Кукуруза":
                cme_output += f"{last_price:.2f}$ corn🌽, "
            elif name == "Соевые бобы":
                cme_output += f"{last_price:.2f}$ soybeans🍈"
        else:
            cme_output += f"Нет данных для {name.lower()}🌾, "

    # Убираем последнюю запятую и пробел
    if cme_output.endswith(", "):
        cme_output = cme_output[:-2]

    return cme_output





def get_latest_data(ticker_dict):
    data = {}
    for name, ticker in ticker_dict.items():
        stock = yf.Ticker(ticker)
        latest_data = stock.history(period="1mo")  # Получаем данные за последний день
        if not latest_data.empty:
            latest_close = latest_data['Close'].iloc[-1]
            data[name] = latest_close
    return data


def get_maex():
    urls = ['https://ru.investing.com/indices/barley-fob-black-sea-index',
            'https://ru.investing.com/indices/wheat-fob-black-sea-index']
    prices = {}
    count = 0
    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        # Отправка GET-запроса
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Создание объекта BeautifulSoup для парсинга
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.find('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]').text
            last_price = soup.find('span', class_='key-info_dd-numeric__ZQFIs').text
            price = price.replace(',', '.')
            last_price = last_price.replace(',', '.')
            if count == 0:
                prices['Barley'] = {'current_price': price, 'last_price': last_price}
            if count == 1:
                prices['Wheat'] = {'current_price': price, 'last_price': last_price}
            count += 1
        else:
            print(f'Ошибка при запросе: {response.status_code}')

    url = 'https://investfuture.ru/russian_indexes/history/4621'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    # Отправка GET-запроса
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-bordered table-hover')
        rows = table.find_all('tr')[1:3]  # выбираем первые две строки с данными
        values = [float(row.find_all('td')[1].text.replace(',', '.')) for row in rows]
        prices['Corn'] = {'current_price': values[0], 'last_price': values[1]}
    else:
        print(f'Ошибка при запросе: {response.status_code}')
    return prices


def get_matif():
    urls = ['https://ru.investing.com/commodities/us-corn?cid=964533',
            'https://ru.investing.com/commodities/milling-wheat-n2', 'https://ru.investing.com/commodities/rapeseed']
    prices = {}
    count = 0
    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        # Отправка GET-запроса
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Создание объекта BeautifulSoup для парсинга
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.find('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]').text
            last_price = soup.find('span', class_='key-info_dd-numeric__ZQFIs').text
            price = price.replace(',', '.')
            last_price = last_price.replace(',', '.')
            if count == 0:
                prices['Corn'] = {'current_price': price, 'last_price': last_price}
            if count == 1:
                prices['Wheat'] = {'current_price': price, 'last_price': last_price}
            if count == 2:
                prices['Rapeseed'] = {'current_price': price, 'last_price': last_price}
            count += 1
        else:
            print(f'Ошибка при запросе: {response.status_code}')
    return prices
# Получение данных
prices_cme = get_cme_matif_prices()
prices = get_prices()

# Форматированный вывод
final_output = (
    f"💵 USD/RUB: {prices.get('usd_rub', 'нет данных')}₽"
    f"💶 EUR/RUB: {prices.get('eur_rub', 'нет данных')}₽\n"
    # f"💹 USD/EUR: {prices.get('usd_eur', 'нет данных')}€\n"
    # f"🇨🇳 USD/CNY: {prices.get('usd_cny', 'нет данных')}¥\n"
    # f"🇹🇷 USD/TRY: {prices.get('usd_try', 'нет данных')}₺\n"
    f"😱 Bitcoin: {prices.get('btc_price', 'нет данных')}$\n"
    f"🛢 Brent Crude Oil: {prices.get('oil_price', 'нет данных')}$\n"
)
# print(final_output)
# f"{prices_cme}\n"

ticker = {
    'Wheat_CHICAGO': 'ZW=F',  # Пшеница на CME
    'Soybeans_CHICAGO': 'ZS=F',  # Соя на CME
    'Corn_CHICAGO': 'ZC=F',  # Кукуруза на CME
    # Рапс на MATIF
}
moex=get_maex()
matif = get_matif()

# Получение последних данных
commodity_data = get_latest_data(ticker)
txt_chicago = f"CHICAGO - {commodity_data['Wheat_CHICAGO']}$ wheat🌾, {commodity_data['Soybeans_CHICAGO']}$ soybeans🍈, {commodity_data['Corn_CHICAGO']}$ corn🌽 "
txt_matif = f"MATIF - {matif['Wheat']['current_price']}$ wheat🌾, {matif['Rapeseed']['current_price']}$ rapeseed🌱, {matif['Corn']['current_price']}$ corn🌽 "
txt_moex=f"MOEX - {moex['Wheat']['current_price']}$ wheat🌾, {moex['Barley']['current_price']}$ barley🥬, {moex['Corn']['current_price']}$ corn🌽 "
