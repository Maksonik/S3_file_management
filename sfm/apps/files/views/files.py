from typing import Annotated

from fastapi import Depends

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
    return service.get_list_files(prefix=prefix, recursive=recursive, max_keys=max_keys)
