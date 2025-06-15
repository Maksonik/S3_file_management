from typing import Annotated

from fastapi import Depends, UploadFile

from sfm.core.integrations.s3.aws.di import get_service
from sfm.core.integrations.s3.base_service import AbstractStorageService

from .router import files_api_v1


@files_api_v1.get("/{prefix}")
async def get_files(
    prefix: str,
    service: Annotated[AbstractStorageService, Depends(get_service)],
    max_keys: int = 10,
    *,
    recursive: bool = False,
) -> None:
    """
    Return a non-empty response if the service works.
    """
    return await service.get_list_files(prefix=prefix, recursive=recursive, max_keys=max_keys)


@files_api_v1.get("/{prefix}/{filename}/download")
async def get_link_download_file(
    prefix: str,
    filename: str,
    service: Annotated[AbstractStorageService, Depends(get_service)],
) -> None:
    return await service.get_link_download_file(prefix=prefix, filename=filename)


@files_api_v1.post("/{prefix}")
async def upload_file(
    prefix: str,
    file: UploadFile,
    service: Annotated[AbstractStorageService, Depends(get_service)],
) -> dict:
    await service.upload_file(prefix=prefix, file=file)
    return {"file_size": len(file.filename)}


@files_api_v1.delete("/{prefix}/{filename}")
async def delete_file(
    prefix: str,
    filename: str,
    service: Annotated[AbstractStorageService, Depends(get_service)],
) -> dict:
    await service.delete_file(prefix=prefix, filename=filename)
    return {"prefix": prefix, "filename": filename}
