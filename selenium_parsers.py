import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


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