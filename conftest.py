import pytest


@pytest.fixture()
def setup_function():
    print('Start testing')

@pytest.fixture()
def teardown_function():
    print('End testing')
