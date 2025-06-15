from io import BytesIO

import pytest
from fastapi import UploadFile
from freezegun import freeze_time

from sfm.core.integrations.s3.schemas import ListFilesResponse
from tests.test_utils.any import ANY_DATETIME, ANY_STR


@pytest.mark.vcr
async def test_get_list_files(aws_service):
    result = await aws_service.get_list_files(prefix="test")
    assert result == ListFilesResponse(files=[], is_truncated=False, next_marker=None)


@pytest.mark.vcr
@freeze_time("2025-06-15")
async def test_get_link_download_file(aws_service):
    result = await aws_service.get_link_download_file(prefix="test", filename="test")
    assert result.model_dump(mode="python") == {"download_url": ANY_STR, "expires_at": ANY_DATETIME}


@pytest.mark.vcr
async def test_delete_file(aws_service):
    result = await aws_service.delete_file(prefix="test", filename="test")
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 204


@pytest.mark.vcr
async def test_upload_file(aws_service):
    file = UploadFile(filename="bad.jpg", file=BytesIO(b"data"))
    result = await aws_service.upload_file(prefix="test", file=file)
    assert result is None
