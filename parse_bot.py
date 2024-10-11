import requests
from bs4 import BeautifulSoup
import openai
import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
load_dotenv()

openai.api_key = os.getenv('openai.api_key')

# Инициализация бота
API_TOKEN = os.getenv('API_TOKEN')

CHANNEL_ID=os.getenv('CHANNEL_ID')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функции для парсинга новостей
def oilworld_parser(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div = soup.find('div', class_='row l-col-news')
    links = news_div.find_all('a')

    set_href = []
    for link in links:
        href = link.get('href')
        set_href.append(f'https://www.oilworld.ru{href}')
    count=0
    oilworld = []
    for i in set(set_href):
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_='pad-left-page')
        title = news_div.find('h2').text
        text_ = news_div.find('div', class_='l-font').text
        oilworld.append(f"Title:\n{title}\nText: {text_}")
        if count == 8:
            break
        count+=1
    return '\n'.join(oilworld[:8])  # Возвращаем первые 6 новости


def zol_parser(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div = soup.find('table', class_='news_block news_list')
    news_div = news_div.find_all('a', class_='news_block')

    set_href = []
    for news in news_div[:6]:  # Ограничим до 6 новостей
        href = news.get('href')
        set_href.append(f'https://www.zol.ru{href}')
    count=0
    zol = []
    for i in set_href:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_='content')
        title = news_div.find('h1', class_='news_one_h1').text
        text_ = news_div.find('div', class_='text_content news_one').text
        zol.append(f"Title:\n{title}\nText: {text_}")
        if count == 8:
            break
        count+=1
    return '\n'.join(zol[:8])  # Возвращаем первые 3 новости


def prozerno_parser(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div = soup.find('ul', class_="latestnews dark")
    news_div = news_div.find_all('a')
    set_href = []
    for news in news_div[:6]:
        href = news.get('href')
        set_href.append(f'https://prozerno.ru{href}')
    prozerno = []
    count=0
    for i in set_href:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_='item-page')
        title = news_div.find('h2').text
        text_ = news_div.find_all('p')
        prozerno.append(f"Title:\n{title}\n" + f'Text: {"".join([p.text for p in text_])}')
        if count == 8:
            break
        count += 1
    return ''.join(prozerno[:8])  # Возвращаем первые 3 новости


def investing_parser(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div = soup.find('div', class_="col col--xs")
    # news_div = news_div.find_all('aside', class_="aside")
    news_div = news_div.find_all('a')

    set_href = []
    for news in news_div[:6]:
        href = news.get('href')
        set_href.append(f'https://www.agroinvestor.ru{href}')
        # print(href)
    investing = []
    count=0
    for i in set_href[:-1]:
        # print(i)
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_='article__header-content')
        # print(news_div)
        title = f'{news_div.find('h1').text}\n{news_div.find('h2').text}'
        # print(title)
        text_ = soup.find('div', class_='col col--xl')
        # print(text_)
        text_ = text_.find_all('p')
        # print(text_)
        if count == 8:
            break
        count+=1
        texts = ''
        for txt in text_:
            texts += txt.text
        #
        investing.append(f"Title:\n{title}\n" + f'Text: {"".join([p.text for p in text_])}')
    # print(investing)
    return ''.join(investing[:8])


def aemcx(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news = []
        posts = soup.find_all('div', class_='w-post-elm post_image usg_post_image_1 stretched')
        for post in posts:
            href = post.find('a')['href']
            news.append(href)
        aemcx = []
        count=0
        for new in news:
            response = requests.get(new)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h2', class_='w-post-elm post_title align_left entry-title color_link_inherit')
            title=title.text
            if count==8:
                break
            count += 1
            text_ = soup.find_all('div', class_='w-post-elm post_content')
            aemcx.append(f"Title:\n{title}\n" + f'Text: {"".join([p.text for p in text_])}')
        return ''.join(aemcx[:8])
    else:
        print(f"Ошибка: {response.status_code}")


def malayzya_tg(url):
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        # pprint.pprint(soup.prettify())
        # Ищем все посты
        # news=[]
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')
        txt = ''
        for post in posts:
            txt += post.text
        return txt[1800:]

def kz_tg(url):
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        # pprint.pprint(soup.prettify())
        # Ищем все посты
        # news=[]
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')
        txt = ''
        for post in posts:
            txt += post.text
        return txt[1800:]

def rusgrain_tg(url):
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все посты
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')
        txt = ''

        for post in posts:
            # Удаляем блоки с ненужным контентом
            for unwanted in post.find_all(['div', 'a'],
                                          class_=['tgme_widget_message_forwarded_from', 'tgme_widget_message_footer']):
                unwanted.decompose()

            # Добавляем текст поста в итоговую переменную
            txt += post.text.strip()

        return txt[1800:]

def minselhoz_tg(url):
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        # pprint.pprint(soup.prettify())
        # Ищем все посты
        # news=[]
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')
        txt = ''
        for post in posts:
            txt += post.text
        return txt[1800:]

# Функция модификации метода __del__ для undetected_chromedriver
def selenium_modified_del(self):

    try:
        self.service.process.kill()
    except Exception:  # noqa
        pass
    try:
        self.quit()
    except OSError:
        pass


uc.Chrome.__del__ = selenium_modified_del


def get_html_data(time_sleep):

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Инициализация драйвера
    driver = uc.Chrome(options=chrome_options)

    website_html_content = []

    try:
        url = 'https://finviz.com/news.ashx'
        driver.get(url)

        # Явное ожидание до полной загрузки элемента
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        time.sleep(time_sleep)  # Подождите, если требуется дополнительное время для загрузки
        html_content = driver.page_source
        website_html_content.append(html_content)

    except Exception as e:
        print(f"Ошибка при сборе данных: {e}")

    finally:
        # Закрытие драйвера
        driver.quit()

    return website_html_content


def parse_html(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')

    # Пример извлечения данных - заголовков новостей
    news_items = soup.find_all('a', class_='nn-tab-link')
    data = []

    for item in news_items:
        title = item.text.strip()
        link = item['href']
        data.append({'Title': title, 'Link': link})

    return data


def get_article_details(driver, link):

    driver.get(link)

    # Явное ожидание до полной загрузки элемента
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Извлечение заголовка и текста статьи
    title = soup.find('title').text if soup.find('title') else 'No Title'
    paragraphs = soup.find_all('p')
    content = ' '.join(p.text for p in paragraphs).strip()

    return {'Title': title, 'Content': content}


def collect_articles_text(time_sleep):

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Инициализация драйвера
    driver = uc.Chrome(options=chrome_options)

    all_articles_text = ""
    articles_collected = 0  # Счётчик статей

    try:
        html_contents = get_html_data(time_sleep)
        for html in html_contents:
            parsed_data = parse_html(html)
            for entry in parsed_data:
                link = entry['Link']
                article_details = get_article_details(driver, link)

                # Проверяем, что контент не пустой
                if article_details['Content'].strip():
                    all_articles_text += f"Title: {article_details['Title']}\n"
                    all_articles_text += f"Content: {article_details['Content']}\n\n"

                    articles_collected += 1
                    # Проверяем, достигли ли мы лимита в 10 статей
                    if articles_collected >= 10:
                        break

            # Если 10 статей уже собрано, прерываем внешний цикл
            if articles_collected >= 10:
                break

    except Exception as e:
        print(f"Ошибка при сборе данных: {e}")

    finally:
        # Закрытие драйвера
        driver.quit()

    return all_articles_text

def agroinvestor(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news = []
        posts = soup.find_all('div', class_='news__item news__item--small')
        for post in posts[:1]:
            href = post.find('a')['href']
            href=f'https://www.agroinvestor.ru{href}'

        response = requests.get(href)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='article__body')
        # print(title.text)
        return(title)

def minselhoz_tg(url):
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все посты
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')

        # Оставляем только последние 6 постов
        last_six_posts = posts[:6]

        # Объединяем тексты постов
        txt = ''
        for post in last_six_posts:
            # Удаляем блоки с ненужной информацией
            for unwanted in post.find_all(['div', 'span', 'a'],
                                          class_=['tgme_widget_message_footer',  # Удаляем блок с количеством просмотров и временем
                                                  'tgme_widget_message_views',   # Удаляем количество просмотров
                                                  'tgme_widget_message_meta',    # Удаляем блок с датой и временем
                                                  'tgme_widget_message_forwarded_from',  # Удаляем блок с названием канала
                                                  'tgme_widget_message_service',
                                                  'tgme_widget_message_reply_header',  # Удаляем уведомления "Please open Telegram to view this post"
                                                  ]):
                unwanted.decompose()

            # Добавляем текст поста в итоговую переменную
            txt += post.text.strip() + '\n\n'

        return txt

def converted_file(url):
    with open(url, 'r', encoding='utf-8') as file:
        return file.read()


def news_archive(url, text):
    with open(url, 'w', encoding='utf-8') as file:
        file.write(text)


# Функция для получения новостей через OpenAI API
async def fetch_news():
    site_1 = oilworld_parser('https://www.oilworld.ru/news/')
    site_2 = prozerno_parser('https://prozerno.ru/')
    site_3 = zol_parser('https://www.zol.ru/news/grain/')
    site_4 = investing_parser('https://www.agroinvestor.ru')
    site_5 = aemcx("https://aemcx.ru/?ysclid=m0dfoaxnro723127004")
    site_6 = malayzya_tg("https://t.me/s/oilpalm")
    site_7 =collect_articles_text(3)
    site_8 =kz_tg('https://t.me/s/ElDalakz')
    site_9 =rusgrain_tg('https://t.me/s/rusgrain')
    site_10 =agroinvestor("https://www.agroinvestor.ru/archive/")
    site_11=minselhoz_tg('https://t.me/s/minselhozrf')
    site_12=minselhoz_tg('https://t.me/s/mcxae')
    prompt = (f"Новости с сайтов:\n\nOilworld:\n{site_1}\n\nProzerno:\n{site_2}\n\nZol.ru:\n{site_3}\nagroinvestor.ru:\n{site_4}"
              f"\naemcx.ru:\n{site_5}\nmalayzya: \n{site_6}\nfinviz.ru\n{site_7}\nkz.ru:\n{site_8}\nrusgrain:\n{site_9}\nagroinvestor\n{site_10}\n"
              f"minselhozrf\n{site_11}\nminselhoz.ru:\n{site_12}")   #
    news_archive('news_archive.txt', prompt)
    file = converted_file(r'example.txt')
    try:
        response = await openai.ChatCompletion.acreate(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "contenf":f'''You are a news analyst. Summarize the key points from the news.
                                                For each news item, include the source of the information below the summary.
                                                The title is not needed, let's have the text in Russian
                                                Omit the date.
                                                Only share news about vegetable oils; skip anything related to butter or dairy.
                                                Place oil-related news last in the list.
                                                Avoid using asterisks (*) or numbering bullet points.
                                                Use emojis in the text to make it more engaging.
                                                Here are examples of how the news should be presented: {file}.'''},
                {"role": "user", "content": prompt},
            ],
            max_tokens=3000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Ошибка OpenAI API: {e}")
        return None


# Функция для отправки сообщений в канал Telegram
async def send_news_to_channel(news):
    if news:
        await bot.send_message(CHANNEL_ID, f'''AGROCOR INFORMS 🌾\n\n{news}\n\n🤝OFFERS ➡➡➡ https://t.me/+F8OsiZiNLg00NTY6\n🚢 VESSEL CATCHER ➡➡➡ https://t.me/+AqsaM2xqhS44NDQy\n🔥💰 TRADER’S STORIES ➡➡➡ https://t.me/+bzwCOPgtSWMyNTQ
''', disable_web_page_preview=True)
    else:
        await bot.send_message(CHANNEL_ID, "Не удалось получить новости на данный момент.")


# Асинхронная задача для регулярной отправки новостей
async def scheduled_news_sender(interval):
    while True:
        news = await fetch_news()
        await send_news_to_channel(news)
        await asyncio.sleep(interval)  # Периодичность обновления новостей (в секундах)


# Основная асинхронная функция, запускающая бота и задачи
async def main():
    asyncio.create_task(scheduled_news_sender(3600 * 24))  # Запускаем задачу для отправки новостей каждые 60 минут
    await dp.start_polling(bot)  # Указываем бота при запуске polling


# Запуск программы
if __name__ == '__main__':
    asyncio.run(main())
