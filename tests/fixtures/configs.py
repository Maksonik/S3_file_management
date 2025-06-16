import logging

import pytest

from tests.constants import TESTSERVER_HOST


@pytest.fixture(scope="session")
def vcr_config():
    """VCR configuration."""

    logging.getLogger("vcr.cassette").setLevel(logging.WARNING)
    logging.getLogger("vcr.stubs").setLevel(logging.WARNING)

    return {
        "record_mode": "none",
        "ignore_hosts": [TESTSERVER_HOST],
        "filter_headers": [
            ("authorization", "DUMMY"),
            ("User-Agent", "User-Agent"),
            ("X-Amz-Content-SHA256", "X-Amz-Content-SHA256"),
            ("X-Amz-Date", "X-Amz-Date"),
            ("amz-sdk-invocation-id", "amz-sdk-invocation-id"),
            ("amz-sdk-request", "amz-sdk-request"),
        ],
        "record_on_exception": False,
    }
