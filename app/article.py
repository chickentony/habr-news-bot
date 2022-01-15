from __future__ import annotations
from typing import List


class Article:
    """Class with information about habr articles"""
    def __init__(self, title: str, link: str, votes: str, views: str):
        if not all(isinstance(argument, str) for argument in (title, link, votes, views)):
            raise ValueError
        self.title = title
        self.link = link
        self.votes = votes
        self.views = views

    @classmethod
    def build_from_list(cls, article_fields: list) -> Article:
        if not isinstance(article_fields, list):
            raise ValueError
        if not article_fields:
            raise ValueError
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
    result_message = ''
    for article in articles_list:
        message_text = f'[{article.title}]({article.link})\n' \
                       f'Количество голосов: {article.votes}\n' \
                       f'Количество просмотров: {article.views}\n\n'
        result_message += message_text
    return result_message
