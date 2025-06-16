from abc import ABC, abstractmethod

from fastapi import UploadFile

from sfm.core.integrations.s3.schemas import DownloadLinkResponse, ListFilesResponse


class AbstractStorageService(ABC):
    @abstractmethod
    async def get_list_files(
        self,
        prefix: str,
        max_keys: int,
        *,
        recursive: bool,
    ) -> ListFilesResponse:
        """
        Get a list of files from the S3 bucket with the given prefix.

        :param prefix: Prefix (folder path) in the bucket to search in.
        :param max_keys: Maximum number of files to return.
        :param recursive: Whether to include files from subdirectories.
        :return: A FilesResponse object containing file metadata and pagination info.
        """

    @abstractmethod
    async def upload_file(self, prefix: str, file: UploadFile) -> None:
        """
        Upload a file to the specified directory in the S3 bucket.

        :param prefix: Target directory (prefix) in the bucket.
        :param file: File to upload.
        :return: Upload result or metadata (implementation-dependent).
        """

    @abstractmethod
    async def delete_file(self, prefix: str, filename: str) -> None:
        """
        Delete a file from the specified directory in the S3 bucket.

        :param prefix: Directory containing the file.
        :param filename: Name of the file to delete.
        :return: Deletion result or confirmation.
        """

    @abstractmethod
    async def get_link_download_file(self, prefix: str, filename: str) -> DownloadLinkResponse:
        """
        Generate a pre-signed temporary download link for a file.

        :param prefix: Directory containing the file.
        :param filename: Name of the file to generate the link for.
        :return: Dictionary with the download URL and expiration timestamp.
        """
