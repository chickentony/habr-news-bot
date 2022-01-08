from unittest.mock import patch, MagicMock

import pytest
import requests

from app.articles_parser import get_website_html_page

MOCK_RESPONSE_DEFAULT_STATUS_CODE = 200


def build_mock_response(text: str, status_code=MOCK_RESPONSE_DEFAULT_STATUS_CODE) -> MagicMock:
    mock_response = MagicMock(
        text=text,
        status_code=status_code
    )
    return mock_response


@patch('requests.get')
def test_get_website_html_page_can_get_website_content_mocked(mock_requests_get):
    mock_requests_get.return_value = build_mock_response('<p>test html</p>')

    response = get_website_html_page('test')

    assert 0 != len(response)


@patch('requests.get')
def test_get_website_html_page_should_raise_exception_if_connection_problems(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.RequestException('test exception')

    with pytest.raises(ConnectionError):
        get_website_html_page('test url')
