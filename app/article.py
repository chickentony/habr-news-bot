from __future__ import annotations
from typing import List


class Article:
    """Class with information about habr articles"""

    def __init__(self, title: str, link: str, votes: str, views: str):
        """
        Init class instance with provided params.

        :raise ValueError if not string params provided
        :param title: article title
        :param link: link to article on habr website
        :param votes: votes count of article. Format: Всего голосов 10: ↑5 и ↓5  0
        :param views: views count of article. Format: Просмотры  8.2K
        """
        if not all(isinstance(argument, str) for argument in (title, link, votes, views)):
            raise ValueError
        self.title = title
        self.link = link
        self.votes = votes
        self.views = views

    @classmethod
    def build_from_list(cls, article_fields: list) -> Article:
        """
        Create new instance of article class from provided list.

        :raises ValueError if not list param provided or if empty list provided,
        IndexError if incorrect number of elements provided in list
        :param article_fields: list with article info
        :return: new Article() instance
        """
        expected_element_count = 4
        if not isinstance(article_fields, list):
            raise ValueError
        if not article_fields:
            raise ValueError
        if len(article_fields) != expected_element_count:
            raise IndexError
        article_title = article_fields[0]
        article_link = article_fields[1]
        articles_votes = article_fields[2]
        articles_views = article_fields[3]

        article = cls(article_title, article_link, articles_votes, articles_views)
        return article

    def __repr__(self):
        _repr = f'{self.__class__.__name__}({self.title}, {self.link}, {self.votes}, {self.views})'
        return _repr

    def __eq__(self, other: Article):
        outcome = (
                self.title == other.title
                and self.link == other.link
                and self.votes == other.votes
                and self.views == other.views
        )
        return outcome


def prepare_message_for_telegram(articles_list: List[Article]) -> str:
    """
    Aggregate information from list of articles info into one text message.
    Example:
    QAчественное общение—4. Выступления спикеров (https://habr.com/ru/company/alfa/blog/598387/)
    Количество голосов: Всего голосов 5: ↑5 и ↓0  +5
    Количество просмотров: Просмотры  400

    :param articles_list: list with articles
    :return: message text
    """
    result_message = ''

    for article in articles_list:
        message_text = f'[{article.title}]({article.link})\n' \
                       f'Количество голосов: {article.votes}\n' \
                       f'Количество просмотров: {article.views}\n\n'
        result_message += message_text

    return result_message
