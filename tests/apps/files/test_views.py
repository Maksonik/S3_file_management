from io import BytesIO

import pytest
from fastapi import status


@pytest.mark.vcr
async def test_get_files_view(test_client):
    response = test_client.get("/v1/files/tests")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "files" in data
    assert "is_truncated" in data


@pytest.mark.vcr
async def test_get_files_view_too_many(test_client):
    for _ in range(20):
        test_client.get("/v1/files/tests")

    response = test_client.get("/v1/files/tests")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.vcr
async def test_upload_file_view(test_client):
    file = BytesIO(b"sample data")
    response = test_client.post(
        "/v1/files/tests",
        files={"file": ("file.jpg", file, "text/plain")},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.vcr
async def test_upload_invalid_file_type(test_client):
    file = BytesIO(b"virus")
    response = test_client.post(
        "/v1/files/tests",
        files={"file": ("malware.exe", file, "application/octet-stream")},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "not allowed" in response.text.lower()


@pytest.mark.vcr
async def test_delete_file_view(test_client):
    response = test_client.delete("/v1/files/tests/test.txt")
    assert response.status_code == status.HTTP_204_NO_CONTENT
