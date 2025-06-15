from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    name: str
    size: int
    last_modified: datetime
    type: str


class FilesResponseModel(BaseModel):
    files: list[FileResponse]
    is_truncated: str
    next_marker: str
