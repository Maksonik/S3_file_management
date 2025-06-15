from typing import Annotated

from fastapi import Depends, File, Path, Query, UploadFile

from sfm.core.integrations.s3.aws.di import get_service
from sfm.core.integrations.s3.base_service import AbstractStorageService

from .router import files_api_v1


@files_api_v1.get("/{prefix}", description="Get files")
async def get_files(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    max_keys: Annotated[int, Query(description="The maximum number of files to get")] = 10,
    *,
    recursive: Annotated[bool, Query(description="Get files recursively")] = False,
) -> None:
    """
    Return a non-empty response if the service works.
    """
    return await service.get_list_files(prefix=prefix, recursive=recursive, max_keys=max_keys)


@files_api_v1.get("/{prefix}/{filename}/download", description="Get link for download a file")
async def get_link_download_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    filename: Annotated[str, Path(description="The name of the file to download")],
) -> None:
    return await service.get_link_download_file(prefix=prefix, filename=filename)


@files_api_v1.post("/{prefix}", description="Upload a file")
async def upload_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    file: Annotated[UploadFile, File(description="The file to upload")],
) -> dict:
    await service.upload_file(prefix=prefix, file=file)
    return {"file_size": len(file.filename)}


@files_api_v1.delete("/{prefix}/{filename}", description="Delete a file")
async def delete_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    filename: Annotated[str, Path(description="The name of the file to download")],
) -> dict:
    await service.delete_file(prefix=prefix, filename=filename)
    return {"prefix": prefix, "filename": filename}
