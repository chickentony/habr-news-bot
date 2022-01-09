import pytest

from app.articles_parser import get_habr_articles_html, parse_habr_articles_content

HABR_URL_TO_PARSE = 'https://habr.com/ru/hub/python/'
HABR_ARTICLES_DUMP_FILEPATH = 'app/tests/tests_data/habr_articles_dump.html'
HABR_EMPTY_ARTICLES_DUMP_FILEPATH = 'app/tests/tests_data/habr_empty_articles_dump.html'


@pytest.fixture(scope='function')
def habr_html_fixture() -> str:
    with open(HABR_ARTICLES_DUMP_FILEPATH, 'r') as fio:
        content = fio.read()
    return content\


@pytest.fixture(scope='function')
def habr_empty_articles_html_fixture() -> str:
    with open(HABR_EMPTY_ARTICLES_DUMP_FILEPATH, 'r') as fio:
        content = fio.read()
    return content


@pytest.mark.integration_test
def test_get_habr_articles_html_can_get_html_page_from_website():
    html_content = get_habr_articles_html(HABR_URL_TO_PARSE)

    assert 0 != len(html_content)
    assert 'python' in html_content


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


def test_parse_habr_articles_content_can_get_articles_data_from_html_content(habr_html_fixture):
    expected_result = [
        ['7 характеристик хороших тестов', ' Очень редко люди задумываются что определяет хорошие тесты. Если тесты отличные то их просто невидно - они прозрачно растворяются в процессе и про них только вспоминают когда они ловят баг.   Читать далее', 'https://habr.com/ru/post/599507/'],
        ['Транзакционное юнит-тестирование приложений с БД', ' \nВ современном мире множество приложений используют трехуровневую архитектуру с базой данных в слоях данных. Наличие юнит-тестов обычно упрощает поддержку продукта, но присутствие базы данных в архитектуре заставляет разработчиков применять смекалку. \n\nВ этой статье я хочу провести обзор разных способов юнит-тестирования приложения с БД и рассказать о способе, который я не видел в русскоязычном сегменте интернета. Статья будет посвящена Python 3, pytest и ORM-фреймворку SQLAlchemy, но методы переносимы на другие инструменты. Читать дальше →', 'https://habr.com/ru/company/selectel/blog/598499/'],
        ['Качество ПО, которое содержит сервис платёжных шлюзов: Что? Где? И как тестировать?', ' Как выйти на рынок с программным продуктом для платёжных операций, который удовлетворит потребности пользователей и гарантирует безопасность транзакций? Рассказываем в этой статье. Читать далее', 'https://habr.com/ru/post/598497/'],
        ['QAчественное общение—4. Выступления спикеров', ' Привет!14 декабря мы провели очередной митап для тестировщиков, QAчественное общение. Спасибо всем, кто подключился. В этом посте мы собрали видео с выступлениями наших спикеров. Если что, вот темы коротко.О чём говорят автотесты?Олег Асмоловский, QA Lead, Test ITАPI тестирование без документации. История про боль, унижения и костылиИгорь Гольшмидт, QA Team Lead, MoovitЗакрой техдолг — устрой Alfa Bugathon!Иван Боклач, QA Lead, Альфа-Банк Читать далее', 'https://habr.com/ru/company/alfa/blog/598387/'],
        ['На пути к идеалу. Как мы приводим тестовое окружение в соответствие с продакшеном', ' Привет, Хабр! Меня зовут Вячеслав Савельев, я отвечаю за разработку ключевых сервисов Учи.ру. Сегодня расскажу, как в процессе постепенного внедрения микросервисов в компании (тут, тут и тут можно прочитать об этом подробнее) мы столкнулись с проблемой конфигурации стейджовых окружений. И вот как мы с ней справились. Читать далее', 'https://habr.com/ru/company/uchi_ru/blog/598035/'],
        ['Что такое тестирование. Курс молодого бойца. Книга для новичков', ' Привет!Меня зовут Ольга Назина. Я в тестировании с 2006 года. Тестировщик, тренер, практик, энтузиаст — вот тут можно почитать обо мне подробнее.Я очень люблю серию книг по разработке ПО от Head First O`Reilly:• Изучаем Java. Кэти Сьерра и Берт Бейтс• Изучаем SQL. Линн Бейли•   и другиеИ вот я решила написать книгу для начинающих тестировщиков. В таком же стиле. С картиночками, примерами, домашними заданиями и всё такое. О ней я и хочу вам рассказать Читать далее', 'https://habr.com/ru/post/597859/'],
        ['Тестировщик — боец невидимого бэка, или Как мы управляли нагрузкой на этих бравых ребят', ' Наш блок разработки планировал цикл «программирование — тестирование — внедрение» только исходя из доступности своих ресурсов. А проектов было много. Тестировщиков ставили перед фактом: мол, есть задача, проверить нужно вчера — погнали. В итоге задачи наслаивались, тестировщики фигачили без перерыва, роптали и сбегали в другие компании. Надо было это прекращать — и мы вышли из положения с помощью Excel. И вот как нам это удалось.    Читать далее', 'https://habr.com/ru/company/rshb/blog/597501/'],
        ['QA Meeting Point 2021: тестирование BigData, развитие команды, тонкости работы с AI', ' 1 декабря мы провели конференцию QA Meeting Point. Участники услышали выступления экспертов в области тестирования AI и BigData, разобрались в основах performance-тестирования, познакомились с GraphQL и узнали, как создавать модульные тестовые проекты.\xa0Ссылка на доклады и видео о QA Meeting Point — под катом.  Читать далее', 'https://habr.com/ru/company/dins/blog/597201/']
    ]
    result = parse_habr_articles_content(habr_html_fixture)

    assert expected_result == result


def test_parse_habr_articles_content_return_empty_list_if_no_articles_found(
        habr_empty_articles_html_fixture
):
    result = parse_habr_articles_content(habr_empty_articles_html_fixture)

    assert [] == result


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
