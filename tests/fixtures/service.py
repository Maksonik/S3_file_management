import pytest

from sfm.core.permissions.rate_limiter import _request_logs
from sfm.core.utils import async_cache


@pytest.fixture
def disable_cache():
    original_value = async_cache.USE_CACHE
    async_cache.USE_CACHE = False
    yield
    async_cache.USE_CACHE = original_value


@pytest.fixture(autouse=True)
def clear_test_limit_rate(aws_service):
    _request_logs.clear()
