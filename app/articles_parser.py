from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HABR_BASE_URL = 'https://habr.com'


def get_habr_articles_html(url: str):
    if not isinstance(url, str):
        raise ValueError
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    html_data = driver.page_source
    return html_data


def parse_habr_articles_content(html_data: str) -> List[List[str]]:
    if not isinstance(html_data, str):
        raise ValueError
    result_articles_list = []
    page_soup = BeautifulSoup(html_data, features='html.parser')
    articles_page = page_soup.find('div', attrs={'class': 'tm-articles-list'})
    if not articles_page:
        return result_articles_list
    articles_data = articles_page.find_all('article')

    for article in articles_data:
        article_snippet = article.find('div', attrs={'class': 'tm-article-snippet'})
        if not article_snippet:
            # ToDo: make construction for different article classes
            # article_snippet = article.find('div', attrs={'class': 'tm-megapost-snippet'})
            continue
        article_header = article_snippet.find('h2')
        article_title = article_header.find('a').get_text()
        article_link = article_header.find('a')['href']
        article_snippet_text = article_snippet.find(
            'div', attrs={'class': 'tm-article-body tm-article-snippet__lead'}
        ).get_text()
        result_articles_list.append(
            [
                article_title,
                article_snippet_text,
                f'{HABR_BASE_URL}{article_link}'
            ]
        )

    return result_articles_list
