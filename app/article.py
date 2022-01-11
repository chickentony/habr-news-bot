from __future__ import annotations
from typing import List


class Article:
    def __init__(self, title: str, snippet: str, link: str):
        self.title = title
        self.snippet = snippet
        self.link = link

    @classmethod
    def build_from_list(cls, article_fields: list) -> Article:
        if not isinstance(article_fields, list):
            raise ValueError
        if not article_fields:
            raise ValueError
        article_title = article_fields[0]
        article_snippet = article_fields[1]
        article_link = article_fields[2]

        article = cls(article_title, article_snippet, article_link)
        return article

    def __repr__(self):
        _repr = f'{self.__class__.__name__}({self.title}, {self.snippet}, {self.link})'
        return _repr

    def __eq__(self, other: Article):
        outcome = (
                self.title == other.title
                and self.snippet == other.snippet
                and self.link == other.link
        )
        return outcome


def prepare_message_for_telegram(articles_list: List[Article]) -> str:
    result_message = ''
    for article in articles_list:
        message_text = f'{article.title} {article.link}\n{article.snippet}\n'
        result_message += message_text
    return result_message
