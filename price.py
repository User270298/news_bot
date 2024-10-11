import yfinance as yf

# Тикеры для биткоина, USD/RUB, EUR/RUB и нефти
tickers = {
    'Bitcoin': 'BTC-USD',
    'USD/RUB': 'USDRUB=X',
    'EUR/RUB': 'EURRUB=X',
    'Brent Crude Oil': 'BZ=F'  # или WTI Crude Oil 'CL=F'
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
            elif name == 'USD/RUB':
                prices['usd_rub'] = round(last_price, 4)
            elif name == 'EUR/RUB':
                prices['eur_rub'] = round(last_price, 3)
            elif name == 'Brent Crude Oil':
                prices['oil_price'] = round(last_price, 2)
        else:
            prices[name] = None  # Если данных нет, присваиваем None

    return prices


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


# Получение данных
prices_cme = get_cme_matif_prices()
prices = get_prices()

# Форматированный вывод
final_output = (
    
    f"💵 USD - {prices.get('usd_rub', 'нет данных')}₽ "
    f"💶 Euro - {prices.get('eur_rub', 'нет данных')}₽ "
    f"😱 Bitcoin – {prices.get('btc_price', 'нет данных')}$ "
    f"🛢 Petroleum – {prices.get('oil_price', 'нет данных')}$"
)
#f"{prices_cme}\n"

ticker = {
    'Wheat_CHICAGO': 'ZW=F',      # Пшеница на CME
    'Soybeans_CHICAGO': 'ZS=F',   # Соя на CME
    'Corn_CHICAGO': 'ZC=F',       # Кукуруза на CME
       # Рапс на MATIF
}
def get_latest_data(ticker_dict):
    data = {}
    for name, ticker in ticker_dict.items():
        stock = yf.Ticker(ticker)
        latest_data = stock.history(period="1mo")  # Получаем данные за последний день
        if not latest_data.empty:
            latest_close = latest_data['Close'].iloc[-1]
            data[name] = latest_close
    return data

# Получение последних данных
commodity_data = get_latest_data(ticker)
txt=f"CHICAGO - {commodity_data['Wheat_CHICAGO']}$ wheat🌾, {commodity_data['Soybeans_CHICAGO']}$ soybeans🍈, {commodity_data['Corn_CHICAGO']}$ corn🌽 "