import pytest
import sys

sys.path.append('./src')

import api  # noqa: E402


@pytest.fixture
def app():
    my_app = api.app.test_client()
    return my_app
