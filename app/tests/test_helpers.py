import pytest

from app.helpers import parse_config

TESTING_CONFIG_FILEPATH = 'app/tests/tests_data/testing_config.yaml'


def test_parse_config_can_parse_config_file():
    expected_value = 'testing value'

    result = parse_config(TESTING_CONFIG_FILEPATH)

    assert 0 != len(result)
    assert expected_value == result['value']


@pytest.mark.parametrize(
    'path_to_config',
    [
        pytest.param(123, id='int'),
        pytest.param(123.0, id='float'),
        pytest.param([], id='list'),
        pytest.param({}, id='dict'),
        pytest.param((), id='tuple'),
        pytest.param(None, id='None'),
    ]
)
def test_parse_config_raise_exception_if_not_str_param_provided(path_to_config):
    with pytest.raises(ValueError):
        parse_config(path_to_config)

