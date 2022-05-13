import pytest
from urllib.request import urlopen

import configs
from app import app

app.testing = True


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_version_is_correct():
    with urlopen('https://malproxy.looga.net/version') as w:
        assert configs.version == w.read().decode('utf-8').strip()[1:-1]
