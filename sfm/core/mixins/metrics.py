from fastapi import UploadFile

from sfm.core import ERROR_COUNT, FILE_UPLOAD_SIZE, REQUEST_COUNT_BY_TYPE_FILE


class MixinMetrics:
    @staticmethod
    def count_type_file(filename: str) -> None:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "unknown"
        REQUEST_COUNT_BY_TYPE_FILE.labels(file_extension=ext).inc()

    @staticmethod
    def count_type_error(status_code: int) -> None:
        ERROR_COUNT.labels(status_code=status_code).inc()

    @staticmethod
    def count_upload_size_file(file: UploadFile) -> None:
        FILE_UPLOAD_SIZE.observe(file.size)

    def count_download_size_file(self, prefix: str, filename: str) -> None:
        response = self.client.head_object(Bucket=self.bucket, Key=f"{prefix}/{filename}")
        FILE_UPLOAD_SIZE.observe(response["ContentLength"])
