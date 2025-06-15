import boto3
from botocore.config import Config
from fastapi import UploadFile

from sfm.core.integrations.s3.aws.schemas import FileResponse, FilesResponse
from sfm.core.integrations.s3.base_service import AbstractStorageService
from sfm.core.settings import Settings


class S3AWSService(AbstractStorageService):
    def __init__(self, settings: Settings):
        self.client = boto3.client(
            "s3",
            region_name=settings.AMAZON.REGION_NAME,
            config=Config(signature_version="s3v4"),
            aws_access_key_id=settings.AMAZON.ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON.SECRET_ACCESS_KEY,
        )
        self.bucket = settings.AMAZON.BUCKET_NAME

    async def get_list_files(
        self,
        prefix: str,
        max_keys: int,
        *,
        recursive: bool,
    ) -> FilesResponse | None:
        paginator = self.client.get_paginator("list_objects_v2")
        operation_parameters = {"Bucket": self.bucket, "Prefix": prefix, "MaxKeys": max_keys}

        page_iterator = paginator.paginate(**operation_parameters)
        files = []
        for page in page_iterator:
            for item in page.get("Contents", []):
                obj_path = item["Key"].strip("/")
                if recursive and f"{prefix}/{obj_path.split('/')[-1]}" != obj_path:
                    continue
                files.append(
                    FileResponse(
                        name=item["Key"],
                        size=item["Size"],
                        last_modified=item["LastModified"].isoformat(),
                        type=item["Key"].split(".")[-1] if "." in item["Key"] else "unknown",
                    ),
                )
            return FilesResponse(
                files=files,
                is_truncated=page.get("IsTruncated", False),
                next_marker=page.get("NextContinuationToken", None),
            )
        return None

    async def upload_file(self, prefix: str, file: UploadFile) -> None:
        self.client.upload_fileobj(file.file, Bucket=self.bucket, Key=f"{prefix}/{file.filename}")

    async def delete_file(self, prefix: str, filename: str) -> None:
        return self.client.delete_object(Bucket=self.bucket, Key=f"{prefix}/{filename}")

    async def get_link_download_file(self, prefix: str, filename: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": f"{prefix}/{filename}",
                "ResponseContentDisposition": f'attachment; filename="{filename}"',
            },
            ExpiresIn=3600,
        )
