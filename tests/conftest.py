import pytest

from tests.core.integrations.s3.aws.fixtures import aws_service
from tests.fixtures import settings, test_client
from tests.fixtures.configs import vcr_config
from tests.fixtures.service import clear_test_dir_from_3s_aws, clear_test_limit_rate

__all__ = [
    "aws_service",
    "clear_test_dir_from_3s_aws",
    "clear_test_limit_rate",
    "settings",
    "test_client",
    "vcr_config",
]

pytestmark = pytest.mark.usefixtures(
    "vcr_config",
)
