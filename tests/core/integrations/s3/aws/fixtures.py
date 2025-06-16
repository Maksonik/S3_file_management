import pytest

from sfm.core.integrations.s3.aws.services import S3AWSService


@pytest.fixture
def aws_service(settings):
    return S3AWSService(settings)
