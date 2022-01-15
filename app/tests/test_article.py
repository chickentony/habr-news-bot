import pytest

from app.article import Article, prepare_message_for_telegram


@pytest.fixture(scope='function')
def articles_fixture():
    articles = [
        Article(
            'Эпические баги прошлого',
            'https://habr.com/ru/post/645133/',
            'Всего голосов 26: ↑25 и ↓1  +24',
            'Просмотры  6.6K'
        ),
        Article(
            'Мониторинг системы мониторинга, или Жизнь внутри индекса',
            'https://habr.com/ru/company/oleg-bunin/blog/599761/',
            'Всего голосов 20: ↑19 и ↓1  +18',
            'Просмотры  2K'
        )
    ]
    return articles


def test_build_from_list_can_create_new_article():
    expected_result = Article(
        'Эпические баги прошлого',
        'https://habr.com/ru/post/645133/',
        'Всего голосов 26: ↑25 и ↓1  +24',
        'Просмотры  6.6K'
    )
    test_data = [
        'Эпические баги прошлого',
        'https://habr.com/ru/post/645133/',
        'Всего голосов 26: ↑25 и ↓1  +24',
        'Просмотры  6.6K'
    ]

    article = Article.build_from_list(test_data)

    assert expected_result == article


@pytest.mark.parametrize(
    'article_fields',
    [
        pytest.param('some string', id='string'),
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
    ]
)
def test_build_from_list_raise_exception_if_not_lst_type_arg_provided(article_fields):
    with pytest.raises(ValueError):
        Article.build_from_list(article_fields)


def test_build_from_list_raise_exception_if_empty_list_arg_provided():
    with pytest.raises(ValueError):
        Article.build_from_list([])


def test_prepare_message_for_telegram_can_aggregate_article_info_for_message(articles_fixture):
    expected_result = '[Эпические баги прошлого](https://habr.com/ru/post/645133/)\n' \
                      'Количество голосов: Всего голосов 26: ↑25 и ↓1  +24\n' \
                      'Количество просмотров: Просмотры  6.6K\n\n' \
                      '[Мониторинг системы мониторинга, или Жизнь внутри индекса]' \
                      '(https://habr.com/ru/company/oleg-bunin/blog/599761/)\n' \
                      'Количество голосов: Всего голосов 20: ↑19 и ↓1  +18\n' \
                      'Количество просмотров: Просмотры  2K\n\n'
    result = prepare_message_for_telegram(articles_fixture)

    assert expected_result == result


@pytest.mark.parametrize(
    'title',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_create_article_raise_exception_if_not_str_title_param_provided(title):
    with pytest.raises(ValueError):
        Article(title, 'test link', 'test votes', 'test views')


@pytest.mark.parametrize(
    'link',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_create_article_raise_exception_if_not_str_link_param_provided(link):
    with pytest.raises(ValueError):
        Article('test title', link, 'test votes', 'test views')


@pytest.mark.parametrize(
    'votes',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_create_article_raise_exception_if_not_str_votes_param_provided(votes):
    with pytest.raises(ValueError):
        Article('test title', 'test link', votes, 'test views')


@pytest.mark.parametrize(
    'views',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_create_article_raise_exception_if_not_str_views_param_provided(views):
    with pytest.raises(ValueError):
        Article('test title', 'test link', 'test votes', views)
