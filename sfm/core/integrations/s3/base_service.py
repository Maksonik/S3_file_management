from abc import ABC, abstractmethod
from typing import Any

from fastapi import File


class AbstractStorageService(ABC):
    @abstractmethod
    async def get_list_files(
        self,
        prefix: str,
        max_keys: int,
        *,
        recursive: bool,
    ) -> Any: ...  # noqa: ANN401

    @abstractmethod
    async def upload_file(self, prefix: str, file: File) -> Any: ...  # noqa: ANN401

    @abstractmethod
    async def delete_file(self, prefix: str, filename: str) -> Any: ...  # noqa: ANN401

    @abstractmethod
    async def get_link_download_file(self, prefix: str, filename: str) -> Any: ...  # noqa: ANN401
