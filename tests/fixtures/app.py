from unittest import mock

import pytest
from starlette.testclient import TestClient

from sfm.core.settings import get_settings


@pytest.fixture(scope="session")
def settings():
    with mock.patch.dict("os.environ"):
        yield get_settings()


@pytest.fixture(scope="session")
def test_client():
    from sfm.core.main import app

    with TestClient(app) as client:
        yield client
