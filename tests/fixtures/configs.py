import logging

import pytest


@pytest.fixture(scope="session")
def vcr_config():
    """VCR configuration."""

    logging.getLogger("vcr.cassette").setLevel(logging.WARNING)
    logging.getLogger("vcr.stubs").setLevel(logging.WARNING)

    return {
        "record_mode": "none",
        "filter_headers": [
            ("authorization", "DUMMY"),
        ],
        "record_on_exception": False,
    }
