import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-integration", action="store_true", default=False, help="skip integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration_test: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-integration"):
        skip_integration = pytest.mark.skip(
            reason="you need to remove --skip-integration option to run"
        )
        for item in items:
            if "integration_test" in item.keywords:
                item.add_marker(skip_integration)
