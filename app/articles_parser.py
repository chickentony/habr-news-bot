import logging
from typing import List, Union, Tuple

import requests
from bs4 import BeautifulSoup, ResultSet

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
        logging.critical('Not string url param provided: %s', url)
        raise ValueError

    try:
        logging.info('Request to habr by url %s', url)
        response = requests.get(url)
    except requests.exceptions.RequestException as exception:
        logging.error("Can't connect to habr. Reason: %s", exception)
        raise ConnectionError from exception

    html_data = response.text
    return html_data


def parse_habr_maegapost(article: ResultSet) -> Tuple[str, str]:
    """
    Parse habr "magapost" articles.

    :param article: ResultSet() class exemplar from bs4 lib
    :return: tuple with article title and link.
    Example: (РСХБ на рейде: собираем профессиональную гильдию тестировщиков, /ru/article/598441/)
    """
    article_megapost_snippet = article.find('div', attrs={'class': 'tm-megapost-snippet'})
    megapost_snippet_wrapper = article_megapost_snippet.find(
        'div', attrs={'class': 'tm-megapost-snippet__wrapper'}
    )
    title_div = megapost_snippet_wrapper.find(
        'div', attrs={'class': 'tm-megapost-snippet__tint'}
    )
    article_title_link = title_div.find(
        'a', attrs={'class': 'tm-megapost-snippet__link tm-megapost-snippet__card'}
    )
    article_title = article_title_link.find('h2').get_text()
    article_link = article_title_link['href']

    return article_title, article_link


def parse_habr_articles_content(html_data: str) -> Union[list, List[Article]]:
    """
    Parse provided HTML page BeautifulSoup lib. Find article title, link, votes and views.
    If on page no articles blocks return empty list.
    For special articles used extend parsing functions.

    :raise ValueError if not string param provided
    :param html_data: habr HTML page
    :return: list contains Article() classes
    """
    if not isinstance(html_data, str):
        logging.critical('Not string html_data param provided: %s', html_data)
        raise ValueError
    result_articles_list = []
    logging.info('Start parsing html data')
    page_soup = BeautifulSoup(html_data, features='html.parser')
    articles_page = page_soup.find('div', attrs={'class': 'tm-articles-list'})
    if not articles_page:
        logging.warning("Return empty list, can't find articles block while parsing html data")
        return result_articles_list
    articles_data = articles_page.find_all('article')

    for article in articles_data:
        article_snippet = article.find('div', attrs={'class': 'tm-article-snippet'})

        if not article_snippet:
            logging.warning('Megapost article found')
            article_title, article_link = parse_habr_maegapost(article)
            logging.info('Finish parsing megapost article')
        else:
            article_header = article_snippet.find('h2')
            article_title = article_header.find('a').get_text()
            article_link = article_header.find('a')['href']

        article_icons = article.find('div', attrs={'class': 'tm-data-icons'})
        article_votes = article_icons.find(
            'div', attrs={'class': 'tm-votes-meter tm-data-icons__item'}
        ).get_text()
        article_views = article_icons.find(
            'span', attrs={'class': 'tm-icon-counter tm-data-icons__item'}
        ).get_text()
        new_article = Article.build_from_list(
            [
                article_title,
                f"{config['habr_base_url']}{article_link}",
                article_votes, article_views
            ]
        )
        result_articles_list.append(new_article)
    logging.info('Finish parsing html data')

    return result_articles_list
