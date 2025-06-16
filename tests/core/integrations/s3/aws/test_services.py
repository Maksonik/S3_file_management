from io import BytesIO

import pytest
from fastapi import UploadFile
from freezegun import freeze_time

from sfm.core.integrations.s3.schemas import ListFilesResponse
from tests.test_utils.any import ANY_DATETIME, ANY_STR


async def clear_test_dir_from_3s_aws(aws_service):
    files = await aws_service.get_list_files(prefix="test")
    for file in files.files:
        name, prefix = file.name.rsplit("/", maxsplit=1)
        await aws_service.delete_file(filename=name, prefix=prefix)


@pytest.mark.vcr(record_mode="once")
async def test_get_list_files(aws_service, disable_cache):
    await clear_test_dir_from_3s_aws(aws_service)

    result = await aws_service.get_list_files(prefix="test")
    assert result == ListFilesResponse(files=[], is_truncated=False, next_marker=None)

    await clear_test_dir_from_3s_aws(aws_service)


@pytest.mark.vcr(record_mode="once")
async def test_get_list_files_recursive(aws_service, disable_cache):
    await clear_test_dir_from_3s_aws(aws_service)

    for index in range(3):
        file = UploadFile(filename=f"{index}_recursive.jpg", file=BytesIO(b"data"))
        await aws_service.upload_file(prefix="test", file=file)
    else:
        recursive_file = UploadFile(filename="recursive_file.jpg", file=BytesIO(b"data"))
        await aws_service.upload_file(prefix="test/recursive", file=recursive_file)

    result = await aws_service.get_list_files(prefix="test", recursive=False)
    assert len(result.files) == 3

    result = await aws_service.get_list_files(prefix="test", recursive=True)
    assert len(result.files) == 4

    await clear_test_dir_from_3s_aws(aws_service)


@pytest.mark.vcr(record_mode="once")
async def test_get_list_files_max_keys(aws_service, disable_cache):
    await clear_test_dir_from_3s_aws(aws_service)

    for index in range(3):
        file = UploadFile(filename=f"{index}_max_keys_file.jpg", file=BytesIO(b"data"))
        await aws_service.upload_file(prefix="test", file=file)

    result = await aws_service.get_list_files(prefix="test", max_keys=1)
    assert len(result.files) == 1

    result = await aws_service.get_list_files(prefix="test", max_keys=10)
    assert len(result.files) == 3

    await clear_test_dir_from_3s_aws(aws_service)


@pytest.mark.vcr
@freeze_time("2025-06-15")
async def test_get_link_download_file(aws_service):
    result = await aws_service.get_link_download_file(prefix="test", filename="test")
    assert result.model_dump(mode="python") == {"download_url": ANY_STR, "expires_at": ANY_DATETIME}


@pytest.mark.vcr(record_mode="once")
async def test_delete_file(aws_service):
    file = UploadFile(filename="deleting_file.jpg", file=BytesIO(b"data"))
    await aws_service.upload_file(prefix="test", file=file)

    result = await aws_service.delete_file(prefix="test", filename="deleting_file.jpg")
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 204


@pytest.mark.vcr
async def test_upload_file(aws_service):
    file = UploadFile(filename="bad.jpg", file=BytesIO(b"data"))
    result = await aws_service.upload_file(prefix="test", file=file)
    assert result is None
