from abc import ABC, abstractmethod
from typing import Any


class AbstractStorageService(ABC):
    @abstractmethod
    def get_list_files(
        self,
        prefix: str,
        max_keys: int,
        *,
        recursive: bool,
    ) -> Any: ...  # noqa: ANN401
