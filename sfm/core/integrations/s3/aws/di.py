from typing import Annotated

from fastapi import Depends

from sfm.core.integrations.s3.aws.services import S3AWSService
from sfm.core.integrations.s3.base_service import AbstractStorageService
from sfm.core.settings import Settings, get_settings


def get_service(settings: Annotated[Settings, Depends(get_settings)]) -> AbstractStorageService:
    return S3AWSService(settings=settings)
