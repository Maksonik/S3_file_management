from datetime import datetime

from pydantic import BaseModel, Field


class DownloadLinkResponse(BaseModel):
    download_url: str = Field(..., description="Pre-signed URL to download the file from S3")
    expires_at: datetime = Field(..., description="Expiration time of the URL in ISO 8601 format (UTC)")


class FileResponse(BaseModel):
    name: str = Field(..., description="Full key (path) of the file in the S3 bucket")
    size: int = Field(..., description="Size of the file in bytes")
    last_modified: datetime = Field(..., description="Last modification timestamp in ISO format")
    type: str = Field(..., description="File type based on the extension (e.g., pdf, txt)")


class ListFilesResponse(BaseModel):
    files: list[FileResponse] = Field(..., description="List of files found under the prefix")
    is_truncated: bool = Field(..., description="True if not all results are returned (pagination)")
    next_marker: str | None = Field(None, description="Pagination marker for the next page if truncated")
