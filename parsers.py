import requests
from bs4 import BeautifulSoup
import chardet


def oilworld_parser(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_='row l-col-news')
        links = news_div.find_all('a')

        set_href = []
        for link in links:
            href = link.get('href')
            set_href.append(f'https://www.oilworld.ru{href}')

        oilworld_news = []
        for i in set(set_href[:6]):
            response = requests.get(i)
            soup = BeautifulSoup(response.text, 'html.parser')
            news_div = soup.find('div', class_='pad-left-page')
            title = news_div.find('h2').text
            text_ = news_div.find('div', class_='l-font').text
            oilworld_news.append({'title': title, 'text': text_})
        return oilworld_news
    except Exception as e:
        print(f"Error in oliworld_parser: {e}")
        return []


def zol_parser(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('table', class_='normal_text news_block')
        # print(news_div)
        news_div = news_div.find_all('a', class_='black_ref')
        zol_news = []
        for news in news_div[:6]:
            href = news.get('href')
            response = requests.get(f'https://www.zol.ru{href}')
            soup = BeautifulSoup(response.text, 'html.parser')
            news_div = soup.find('div', class_='content')
            title = news_div.find('h1', class_='news_one_h1').text
            text_ = news_div.find('div', class_='text_content news_one').text
            zol_news.append({'title': title, 'text': text_})
        return zol_news
    except Exception as e:
        print(f"Error in zol_parser: {e}")
        return []


#
# zol_parser('https://www.zol.ru')

def prozerno_parser(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('ul', class_="latestnews dark")
        news_div = news_div.find_all('a')
        prozerno_news = []
        for news in news_div[:6]:
            href = news.get('href')
            response = requests.get(f'https://prozerno.ru{href}')
            soup = BeautifulSoup(response.text, 'html.parser')
            news_div = soup.find('div', class_='item-page')
            title = news_div.find('h2').text
            text_ = news_div.find_all('p')
            prozerno_news.append({'title': title, 'text': "".join([p.text for p in text_])})
        return prozerno_news
    except Exception as e:
        print(f"Error in prozerno_parser: {e}")
        return []


def agroinvestor_parser(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find('div', class_="col col--xs")
        news_div = news_div.find_all('a')
        investing_news = []
        for news in news_div[:6]:
            href = news.get('href')
            response = requests.get(f'https://www.agroinvestor.ru{href}')
            soup = BeautifulSoup(response.text, 'html.parser')
            news_div = soup.find('div', class_='article__header-content')
            title = news_div.find('h1').text
            subtitle = news_div.find('h2').text if news_div.find('h2') else ""
            full_title = f'{title}\n{subtitle}'
            text_ = soup.find('div', class_='col col--xl').find_all('p')
            text_content = "".join([p.text for p in text_])
            investing_news.append({'title': full_title, 'text': text_content})
        return investing_news
    except Exception as e:
        print(f"Error in agroinvestor_parser: {e}")
        return []


def aemcx_parser(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news = []
            posts = soup.find_all('div', class_='w-post-elm post_image usg_post_image_1 stretched')
            for post in posts:
                href = post.find('a')['href']
                news.append(href)
            aemcx = []
            count = 0
            for new in news:
                response = requests.get(new)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('h2', class_='w-post-elm post_title align_left entry-title color_link_inherit')
                title = title.text
                if count == 8:
                    break
                count += 1
                text_ = soup.find_all('div', class_='w-post-elm post_content')
                aemcx.append(f"Title:\n{title}\n" + f'Text: {"".join([p.text for p in text_])}')
            return ''.join(aemcx[:8])
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Error in aemcx_parser: {e}")
        return []


def agroinvestor(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news = []
            posts = soup.find_all('div', class_='news__item news__item--small')
            for post in posts[:4]:
                href = post.find('a')['href']
                href = f'https://www.agroinvestor.ru{href}'

            response = requests.get(href)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('div', class_='article__body')
            return title
    except Exception as e:
        print(f"Error in agroinvestor: {e}")
        return []


from pprint import pprint


def oleoscope(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='archive-list')
        hrefs = []
        for post in posts:
            # Ищем все ссылки в пределах каждой новости
            links = post.find_all('a')  # Находим все теги <a> в пределах блока новости
            for link in links[:6]:
                href = link['href']  # Получаем ссылку из атрибута href
                # print(href)
                hrefs.append(href)
        oleo = []
        for href in hrefs:
            response = requests.get(href)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', class_='details__title')
            text_ = soup.find('div', class_='details__content content').find_all('p')
            text_content = "".join([p.text for p in text_])
            oleo.append({'title': title.text, 'text': text_content})
        return oleo
    except Exception as e:
        print(f"Error in oleoscope: {e}")
        return []


def parse_tg_channel(url, num_posts=6):
    try:
        """
        Универсальная функция для парсинга последних постов с Telegram-страницы.
    
        :param url: URL страницы Telegram.
        :param num_posts: Количество постов для парсинга (по умолчанию 6).
        :return: Список словарей с заголовками и текстами последних постов.
        """
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code} при обращении к {url}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Найдем все посты
        posts = soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')

        # Если постов меньше, чем ожидаем, парсим всё, что есть
        last_posts = posts[:num_posts]

        news_list = []
        for post in last_posts:
            # Удаляем ненужные блоки
            for unwanted in post.find_all(['div', 'span', 'a'],
                                          class_=['tgme_widget_message_author accent_color',
                                                  'tgme_widget_message_footer compact js-message_footer',
                                                  'tgme_widget_message_meta',
                                                  'tgme_widget_message_forwarded_from',
                                                  'tgme_widget_message_service',
                                                  'tgme_widget_message_reply_header']):
                unwanted.decompose()

            # Получаем заголовок, если есть, или используем "Без заголовка"
            title = post.find('div', class_='tgme_widget_message_user')
            if title:
                title = title.text.strip()
            else:
                title = "Без заголовка"

            # Получаем текст поста
            text = post.text.strip()
            news_list.append({'title': title, 'text': text})

        return news_list
    except Exception as e:
        print(f"Error in parse_tg_channel: {e}")
        return []


def format_news(source, news_list):
    """
    Форматирует список новостей в нужный формат.

    :param source: Название источника.
    :param news_list: Список словарей с заголовками и текстами новостей.
    :return: Отформатированная строка новостей.
    """
    formatted_news = f"{source}\n"
    for index, news in enumerate(news_list):
        title = news.get('title', 'Без заголовка')
        text = news.get('text', 'Без информации')
        formatted_news += f"Заголовок {index + 1} новости:\n{title}\nИнформация по {index + 1} новости:\n{text}\n\n"
    return formatted_news


def tg_channel():
    try:
        # URLs каналов
        channels = {
            "minselhozrf": 'https://t.me/s/minselhozrf',
            "oilpalm": 'https://t.me/s/oilpalm',
            "ElDalakz": 'https://t.me/s/ElDalakz',
            "Rusgrain": 'https://t.me/s/rusgrain',
            'mcxae': 'https://t.me/s/mcxae'
        }

        all_news = ""
        for source, url in channels.items():
            news_list = parse_tg_channel(url)
            formatted_news = format_news(f"Источник: {url}", news_list)
            all_news += formatted_news

        # Выводим все новости
        return all_news
    except Exception as e:
        print(f"Error in tg_channel: {e}")
        return []


from pprint import pprint


def agrotrend_parse(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find('div', class_='announce-list')
        articles = posts.find_all("a", class_="announce-list__item")
        hrefs = []
        for article in articles[:4]:
            link = article.get('href')
            hrefs.append(link)
        agro = []
        for href in hrefs:
            response = requests.get(href)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('div', class_='article-headlines')
            title = title.find('h1').text.strip()
            text_ = soup.find('div', class_='content')
            full_text = text_.get_text(separator="\n", strip=True)
            agro.append({'title': title, 'text': full_text})
        return agro
    except Exception as e:
        print(f"Error in agrotrend_parse: {e}")
        return []


# pprint(agrotrend_parse('https://agrotrend.ru/?s=Зерно'))

def interfaks_parse(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find('div', class_='timeline')
        articles = posts.find_all("a")
        hrefs = []
        for article in articles[:6]:
            link = article.get('href')
            hrefs.append(f'https://www.interfax{link}')
        # print(hrefs)
        inter = []
        for href in hrefs:
            response = requests.get(href)
            detected_encoding = chardet.detect(response.content)['encoding']

            # Устанавливаем найденную кодировку
            response.encoding = detected_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('div', class_='infinitblock')
            title_ = title.find('h1').text.strip()

            text_content = "".join([p.text for p in title])
            inter.append({'title': title_, 'text': text_content})

        return inter
    except Exception as e:
        print(f"Error in interfaks_parse: {e}")
        return []


def zmp_parse(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        posts = soup.find('div',
                          class_='view view--name-webks-inhalt-unterseiten view--display-block-card js-view-dom-id-3781d327ad6db7b0fde1460c55aba22f4ce0ea8ab28635733ce794519c981868')
        # print(posts)
        articles = posts.find_all("a")
        hrefs = []
        for article in articles[:6]:
            link = article.get('href')
            hrefs.append(f'https://www.zmp.de{link}')
        # print(hrefs)
        inter = []
        for href in hrefs:
            response = requests.get(href)
        #     detected_encoding = chardet.detect(response.content)['encoding']
        #
        #     # Устанавливаем найденную кодировку
        #     response.encoding = detected_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.prettify())
        #     title = soup.find('div', class_='infinitblock')
        #     title_=title.find('h1').text.strip()
        #
        #     text_content = "".join([p.text for p in title])
        #     inter.append({'title': title_, 'text': text_content})

        # return inter
    except Exception as e:
        print(f"Error in interfaks_parse: {e}")
        return []

def agroxxi_parse(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='col-12 col-sm-12 col-md-8 col-lg-8')
        hrefs = []
        for post in posts:
            articles = post.find_all("a")
            for article in articles:

                link = article.get('href')
                hrefs.append(f'https://www.agroxxi.ru{link}')
        temp = []
        for x in hrefs:
            if x not in temp:
                temp.append(x)
        hrefs = temp
        agroxxi = []
        for href in hrefs[:6]:
            response = requests.get(href)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', class_='con_heading')
            title = title.text
            txt=soup.find_all('div', class_='articleBody con_text')
            text_content = "".join([p.text for p in txt])
            agroxxi.append({'title': title, 'text': text_content})
        return agroxxi
    except Exception as e:
        print(f"Error in interfaks_parse: {e}")
        return []

# agroxxi_news=agroxxi_parse('https://www.agroxxi.ru/mirovye-agronovosti')
# formatted_agroxxi_news=format_news('Источник: https://www.agroxxi.ru', agroxxi_news)
# print(formatted_agroxxi_news)
# oilworld_news = oilworld_parser('https://www.oilworld.ru/')
# zol_news = zol_parser('https://www.zol.ru/')
# prozerno_news = prozerno_parser('https://prozerno.ru/')
# investing_news = agroinvestor_parser('https://www.agroinvestor.ru/')
# oleoscope_news= oleoscope('https://oleoscope.com/news/')
# agrotrend_news=agrotrend_parse('https://agrotrend.ru/?s=Зерно')
# interfaks_news=interfaks_parse('https://www.interfax.ru/business/')
# # aemcx_news = aemcx_parser('https://www.aemcx.com/')
# formatted_oilworld_news = format_news('Источник: https://www.oilworld.ru', oilworld_news)
# formatted_zol_news = format_news('Источник: https://www.zol.ru', zol_news)
# formatted_prozerno_news = format_news('Источник: https://prozerno.ru', prozerno_news)
# formatted_investing_news = format_news('Источник: https://www.agroinvestor.ru', investing_news)
# formatted_oleoscope_news = format_news('Источник: https://oleoscope.com', oleoscope_news)
# formatted_agrotrend_news = format_news('Источник: https://agrotrend.ru', agrotrend_news)
# formatted_interfax_news = format_news('Источник: https://www.interfax.ru', interfaks_news)
# formatted_tg_channel = tg_channel()
# prompt = (
#     f"Новости с сайтов: \n{formatted_zol_news}\n{formatted_prozerno_news}\n{formatted_investing_news}\n{formatted_tg_channel}\n{formatted_oilworld_news}\n{formatted_oleoscope_news}\n{formatted_agrotrend_news}\n{formatted_interfax_news}")  #
# 
# print(prompt)
