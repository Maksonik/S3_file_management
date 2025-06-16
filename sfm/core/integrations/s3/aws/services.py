from datetime import UTC, datetime, timedelta

import boto3
from botocore.config import Config
from fastapi import HTTPException, UploadFile
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from sfm.core.constants import FILE_TYPE_IS_NOT_ALLOWED
from sfm.core.integrations.s3.base_service import AbstractStorageService
from sfm.core.integrations.s3.schemas import DownloadLinkResponse, FileResponse, ListFilesResponse
from sfm.core.logger import logger
from sfm.core.settings import Settings
from sfm.core.utils.async_cache import async_cache


class S3AWSService(AbstractStorageService):
    def __init__(self, settings: Settings):
        self.client = boto3.client(
            "s3",
            region_name=settings.AMAZON.REGION_NAME,
            config=Config(signature_version="s3v4"),
            aws_access_key_id=settings.AMAZON.ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON.SECRET_ACCESS_KEY,
        )
        self.bucket = settings.S3_BUCKET_NAME
        self.allowed_file_types = settings.ALLOWED_FILE_TYPES

    @async_cache(ttl=300)
    async def get_list_files(
        self,
        prefix: str,
        max_keys: int = 10,
        *,
        recursive: bool = False,
    ) -> ListFilesResponse:
        paginator = self.client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix=prefix, MaxKeys=max_keys)
        page = next(iter(page_iterator))

        files = []
        for item in page.get("Contents", []):
            obj_path = item["Key"].strip("/")
            if not recursive and f"{prefix}/{obj_path.split('/')[-1]}" != obj_path:
                continue
            files.append(
                FileResponse(
                    name=item["Key"],
                    size=item["Size"],
                    last_modified=item["LastModified"].isoformat(),
                    type=item["Key"].split(".")[-1] if "." in item["Key"] else "unknown",
                ),
            )

        logger.info(f"Got list of files in directory {prefix}")
        return ListFilesResponse(
            files=files,
            is_truncated=page.get("IsTruncated", False),
            next_marker=page.get("NextContinuationToken", None),
        )

    async def upload_file(self, prefix: str, file: UploadFile) -> None:
        logger.info(f"Uploading file in directory {prefix}")
        ext = file.filename.rsplit(".", 1)[-1].lower()

        if ext not in self.allowed_file_types:
            logger.info(f"Unsupported file type: {ext}")
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=FILE_TYPE_IS_NOT_ALLOWED.format(ext=ext, allowed_file_types=self.allowed_file_types),
            )

        response = self.client.upload_fileobj(file.file, Bucket=self.bucket, Key=f"{prefix}/{file.filename}")
        logger.info(f"Uploaded file {file.filename}")
        return response

    async def delete_file(self, prefix: str, filename: str) -> None:
        response = self.client.delete_object(Bucket=self.bucket, Key=f"{prefix}/{filename}")
        logger.info(f"Deleted file in directory {prefix}/{filename}")
        return response

    async def get_link_download_file(self, prefix: str, filename: str) -> DownloadLinkResponse:
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": f"{prefix}/{filename}",
                "ResponseContentDisposition": f'attachment; filename="{filename}"',
            },
            ExpiresIn=3600,
        )
        logger.info(f"Generate url for download of file {prefix}/{filename}")
        return DownloadLinkResponse(
            download_url=url,
            expires_at=datetime.now(tz=UTC) + timedelta(seconds=3600),
        )
