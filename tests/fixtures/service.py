import pytest

from sfm.core.permissions.rate_limiter import _request_logs


@pytest.fixture(autouse=True)
def clear_test_dir_from_3s_aws(aws_service):
    aws_service.delete_file(prefix="", filename="test")


@pytest.fixture(autouse=True)
def clear_test_limit_rate(aws_service):
    _request_logs.clear()
