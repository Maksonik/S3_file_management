import pytest

from tests.fixtures import settings, test_client
from tests.fixtures.configs import vcr_config

__all__ = ["settings", "test_client", "vcr_config"]

pytestmark = pytest.mark.usefixtures(
    "vcr_config",
)
