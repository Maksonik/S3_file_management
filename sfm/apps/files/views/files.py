from typing import Annotated

from fastapi import Depends, File, Path, Query, UploadFile

from sfm.core.integrations.s3.aws.di import get_service
from sfm.core.integrations.s3.base_service import AbstractStorageService
from sfm.core.integrations.s3.schemas import FilesResponse

from .router import files_api_v1


@files_api_v1.get("/{prefix}", description="Get files")
async def get_files(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    max_keys: Annotated[int, Query(description="The maximum number of files to get")] = 10,
    *,
    recursive: Annotated[bool, Query(description="Get files recursively")] = False,
) -> FilesResponse:
    """
    Returns a list of files located under the specified prefix in the S3 bucket.
    """
    return await service.get_list_files(prefix=prefix, recursive=recursive, max_keys=max_keys)


@files_api_v1.get("/{prefix}/{filename}/download", description="Get link for download a file")
async def get_link_download_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    filename: Annotated[str, Path(description="The name of the file to download")],
) -> None:
    """
    Generates and returns a temporary download link for a file stored in S3.
    """
    return await service.get_link_download_file(prefix=prefix, filename=filename)


@files_api_v1.post("/{prefix}", description="Upload a file")
async def upload_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    file: Annotated[UploadFile, File(description="The file to upload")],
) -> dict:
    """
    Uploads a file to the specified S3 directory. Validates the file type.
    """
    await service.upload_file(prefix=prefix, file=file)
    return {"file_size": len(file.filename)}


@files_api_v1.delete("/{prefix}/{filename}", description="Delete a file")
async def delete_file(
    service: Annotated[AbstractStorageService, Depends(get_service)],
    prefix: Annotated[str, Path(description="The prefix of the files to get")],
    filename: Annotated[str, Path(description="The name of the file to download")],
) -> dict:
    """
    Deletes a file from the specified prefix (folder) in the S3 bucket.
    """
    await service.delete_file(prefix=prefix, filename=filename)
    return {"prefix": prefix, "filename": filename}
