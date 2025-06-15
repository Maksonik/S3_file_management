import pytest

from tests.core.integrations.s3.aws.fixtures import aws_service
from tests.fixtures import settings, test_client
from tests.fixtures.configs import vcr_config

__all__ = ["aws_service", "settings", "test_client", "vcr_config"]

pytestmark = pytest.mark.usefixtures(
    "vcr_config",
)
