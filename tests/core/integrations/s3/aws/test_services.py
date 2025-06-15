from datetime import UTC
from io import BytesIO

import pytest
from fastapi import UploadFile
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from sfm.core.integrations.s3.schemas import DownloadLinkResponse, ListFilesResponse


@pytest.mark.vcr
async def test_get_list_files(aws_service):
    result = await aws_service.get_list_files(prefix="test")
    assert result == ListFilesResponse(files=[], is_truncated=False, next_marker=None)


@pytest.mark.vcr
@freeze_time("2025-06-15")
async def test_get_link_download_file(aws_service):
    result = await aws_service.get_link_download_file(prefix="test", filename="test")
    assert result == DownloadLinkResponse(
        download_url="https://test-buket-maksonik.s3.amazonaws.com/test/test?response-content-disposition=attachment%3B%20filename%3D%22test%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=%2F20250615%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20250615T000000Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e430cf45f7485a97549aefbe0a50573c9173bd237d0a2372e2b3c737fb7a7199",
        expires_at=FakeDatetime(2025, 6, 15, 1, 0, tzinfo=UTC),
    )


@pytest.mark.vcr
async def test_delete_file(aws_service):
    result = await aws_service.delete_file(prefix="test", filename="test")
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 204


@pytest.mark.vcr
async def test_upload_file(aws_service):
    file = UploadFile(filename="bad.jpg", file=BytesIO(b"data"))
    result = await aws_service.upload_file(prefix="test", file=file)
    assert result is None
