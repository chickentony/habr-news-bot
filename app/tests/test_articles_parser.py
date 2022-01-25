from unittest.mock import patch

import pytest
import requests

from app.articles_parser import get_habr_articles_html, parse_habr_articles_content
from app.article import Article

HABR_URL_TO_PARSE = 'https://habr.com/ru/hub/python/'
HABR_ARTICLES_DUMP_FILEPATH = 'app/tests/tests_data/habr_articles_dump.html'
HABR_EMPTY_ARTICLES_DUMP_FILEPATH = 'app/tests/tests_data/habr_empty_articles_dump.html'


@pytest.fixture(scope='function')
def habr_article_html_fixture() -> str:
    with open(HABR_ARTICLES_DUMP_FILEPATH, 'r') as fio:
        content = fio.read()
    return content


@pytest.fixture(scope='function')
def habr_empty_article_html_fixture() -> str:
    with open(HABR_EMPTY_ARTICLES_DUMP_FILEPATH, 'r') as fio:
        content = fio.read()
    return content


@pytest.mark.integration_test
def test_get_habr_articles_html_can_get_html_page_from_website():
    expected_word_in_search = 'python'

    html_content = get_habr_articles_html(HABR_URL_TO_PARSE)

    assert 0 != len(html_content), (
        f'Content length must be greater then 0'
    )
    assert expected_word_in_search in html_content, (
        f'Searching word {expected_word_in_search} must be in result content'
    )


@patch('requests.get')
def test_get_habr_articles_html_raise_exception_if_external_service_not_available(
        mock_requests_get
):
    mock_requests_get.side_effect = requests.exceptions.RequestException

    with pytest.raises(ConnectionError):
        get_habr_articles_html(HABR_URL_TO_PARSE)


@pytest.mark.parametrize(
    'url',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_get_habr_articles_html_raise_exception_if_not_str_param_provided(url):
    with pytest.raises(ValueError):
        get_habr_articles_html(url)


def test_parse_habr_articles_content_can_get_articles_data_from_html_content(
        habr_article_html_fixture
):
    expected_result = [
        Article('Эпические баги прошлого', 'https://habr.com/ru/post/645133/', 'Всего голосов 26: ↑25 и ↓1  +24', 'Просмотры  6.6K'),
        Article('Мониторинг системы мониторинга, или Жизнь внутри индекса', 'https://habr.com/ru/company/oleg-bunin/blog/599761/', 'Всего голосов 20: ↑19 и ↓1  +18', 'Просмотры  2K'),
        Article('Захватываем сеть через сервер централизованного управления и защищаемся от таких атак', 'https://habr.com/ru/company/bastion/blog/598769/', 'Всего голосов 27: ↑27 и ↓0  +27', 'Просмотры  6.7K'),
        Article('Что случилось с faker.js?', 'https://habr.com/ru/post/599767/', 'Всего голосов 31: ↑27 и ↓4  +23', 'Просмотры  15K'),
        Article('7 характеристик хороших тестов', 'https://habr.com/ru/post/599507/', 'Всего голосов 13: ↑9 и ↓4  +5', 'Просмотры  7.9K'),
        Article('Транзакционное юнит-тестирование приложений с БД', 'https://habr.com/ru/company/selectel/blog/598499/', 'Всего голосов 40: ↑40 и ↓0  +40', 'Просмотры  3.8K'),
        Article('Беда “войти в айти” или курсы тестировщика отзывы: 5-минутный тест на перспективы в QA', 'https://habr.com/ru/post/598481/', 'Всего голосов 8: ↑3 и ↓5  -2', 'Просмотры  25K'),
        Article('Как настроить Pipeline для Jenkins, Selenoid, Allure', 'https://habr.com/ru/company/simbirsoft/blog/597703/', 'Всего голосов 4: ↑3 и ↓1  +2', 'Просмотры  3.9K'),
        Article('Качество ПО, которое содержит сервис платёжных шлюзов: Что? Где? И как тестировать?', 'https://habr.com/ru/post/598497/', 'Рейтинг  0', 'Просмотры  1.4K'),
        Article('РСХБ на рейде: собираем профессиональную гильдию тестировщиков', 'https://habr.com/ru/article/598441/', 'Всего голосов 21: ↑18 и ↓3  +15', 'Просмотры  8.9K'),
        Article('Кроссплатформенный путь мобильного тестировщика или как стать Flutter QA', 'https://habr.com/ru/company/atisu/blog/598389/', 'Всего голосов 10: ↑10 и ↓0  +10', 'Просмотры  6.5K'),
        Article('QAчественное общение—4. Выступления спикеров', 'https://habr.com/ru/company/alfa/blog/598387/', 'Всего голосов 5: ↑5 и ↓0  +5', 'Просмотры  379'),
        Article('Почему разработчик не может быть тестировщиком (или может?)', 'https://habr.com/ru/post/598275/', 'Всего голосов 10: ↑5 и ↓5  0', 'Просмотры  8.2K'),
        Article('Как жить без документации. Если бы реальность тестировщика была сюжетом аниме', 'https://habr.com/ru/post/598169/', 'Всего голосов 3: ↑0 и ↓3  -3', 'Просмотры  8K'),
        Article('На пути к идеалу. Как мы приводим тестовое окружение в соответствие с продакшеном', 'https://habr.com/ru/company/uchi_ru/blog/598035/', 'Всего голосов 2: ↑1 и ↓1  0', 'Просмотры  1.4K'),
        Article('Что такое тестирование. Курс молодого бойца. Книга для новичков', 'https://habr.com/ru/post/597859/', 'Всего голосов 31: ↑29 и ↓2  +27', 'Просмотры  13K'),
        Article('Что учить новичку в QA (тестировании)? Самые распространенные на HeadHunter технологии', 'https://habr.com/ru/post/597573/', 'Всего голосов 7: ↑3 и ↓4  -1', 'Просмотры  12K'),
        Article('Тестировщик — боец невидимого бэка, или Как мы управляли нагрузкой на этих бравых ребят', 'https://habr.com/ru/company/rshb/blog/597501/', 'Всего голосов 8: ↑7 и ↓1  +6', 'Просмотры  3.3K'),
        Article('Начало работы с Playwright (Часть 1)', 'https://habr.com/ru/post/597293/', 'Всего голосов 10: ↑9 и ↓1  +8', 'Просмотры  1.4K'),
        Article('QA Meeting Point 2021: тестирование BigData, развитие команды, тонкости работы с AI', 'https://habr.com/ru/company/dins/blog/597201/', 'Всего голосов 7: ↑6 и ↓1  +5', 'Просмотры  833'),
    ]
    expected_result_len = len(expected_result)

    result = parse_habr_articles_content(habr_article_html_fixture)
    result_len = len(result)

    assert result_len == expected_result_len, (
        f'Length of result lists are no equals, result length {result_len} '
        f'and expected_result length {expected_result_len}'
    )
    assert expected_result == result, (
        f'Expected result: {expected_result} while yours: {result}'
    )


def test_parse_habr_articles_content_return_empty_list_if_no_articles_found(
        habr_empty_article_html_fixture
):
    result = parse_habr_articles_content(habr_empty_article_html_fixture)

    assert [] == result, (
        f'Empty list expected while yours result: {result}'
    )


@pytest.mark.parametrize(
    'html_content',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_parse_habr_articles_content_raise_exception_if_not_str_param_provided(html_content):
    with pytest.raises(ValueError):
        parse_habr_articles_content(html_content)
