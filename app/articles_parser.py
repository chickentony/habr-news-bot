from typing import List, Union

import requests
from bs4 import BeautifulSoup

from app.article import Article
from app.helpers import parse_config

HABR_BASE_URL = 'https://habr.com'
PATH_TO_CONFIG_FILE = 'config.yaml'
config = parse_config(PATH_TO_CONFIG_FILE)


def get_habr_articles_html(url: str) -> str:
    """
    Get page HTML from habr.

    :raises ValueError if not sting param provided,
    ConnectionError if external service not available
    :param url: habr url
    :return: HTML page
    """
    if not isinstance(url, str):
        raise ValueError

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        raise ConnectionError

    html_data = response.text
    return html_data


def parse_habr_articles_content(html_data: str) -> Union[list, List[Article]]:
    """
    Parse provided HTML page BeautifulSoup lib. Find article title, link, votes and views.
    If on page no articles blocks return empty list.

    :raise ValueError if not string param provided
    :param html_data: habr HTML page
    :return: list contains Article() classes
    """
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
        article_icons = article.find('div', attrs={'class': 'tm-data-icons'})
        if not article_snippet:
            continue
        article_votes = article_icons.find(
            'div', attrs={'class': 'tm-votes-meter tm-data-icons__item'}
        ).get_text()
        article_views = article_icons.find(
            'span', attrs={'class': 'tm-icon-counter tm-data-icons__item'}
        ).get_text()
        new_article = Article.build_from_list(
            [article_title, f"{config['habr_base_url']}{article_link}", article_votes, article_views]
        )
        result_articles_list.append(new_article)

    return result_articles_list
