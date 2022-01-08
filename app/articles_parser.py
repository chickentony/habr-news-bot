import requests
from bs4 import BeautifulSoup


def get_website_html_page(url: str) -> str:
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise ConnectionError

    text_response = response.text
    print(text_response)
    return text_response


def parse_content(html_data: str):
    page_soup = BeautifulSoup(html_data, features='html.parser')
    articles_page = page_soup.find('div', attrs={'class': 'tm-articles-list'})
    articles_data = articles_page.find_all('article')
    result_articles_list = []

    for article in articles_data:
        article_snippet = article.find('div', attrs={'class': 'tm-article-snippet'})
        if not article_snippet:
            # article_snippet = article.find('div', attrs={'class': 'tm-megapost-snippet'})
            continue
        article_header = article_snippet.find('h2')
        article_title = article_header.find('a').get_text()
        article_link = article_header.find('a')['href']
        result_articles_list.append([article_title, article_link])

    return result_articles_list


data = get_website_html_page('https://habr.com/ru/hub/it_testing/')
res = parse_content(data)
print(res)