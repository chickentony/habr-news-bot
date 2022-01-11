import pytest

from app.article import Article, prepare_message_for_telegram


@pytest.fixture(scope='function')
def articles_fixture():
    articles = [
        Article('test title', 'some text for snippet', 'some link'),
        Article('test title 2', 'some text for snippet', 'some link')
    ]
    return articles


def test_build_from_list_can_create_new_article():
    expected_result = Article('test', 'some text for snippet', 'some link')
    test_data = ['test', 'some text for snippet', 'some link']

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
    expected_result = 'test title some link\nsome text for snippet\n' \
                      'test title 2 some link\nsome text for snippet\n'

    result = prepare_message_for_telegram(articles_fixture)

    assert expected_result == result
