from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    name: str
    size: int
    last_modified: datetime
    type: str


class FilesResponse(BaseModel):
    files: list[FileResponse]
    is_truncated: bool
    next_marker: str | None = None
