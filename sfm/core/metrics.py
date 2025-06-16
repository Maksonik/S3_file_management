from prometheus_client import Counter, Histogram

REQUEST_COUNT_BY_TYPE_FILE = Counter(
    "file_upload_count_total",
    "Total number of uploaded files grouped by file extension",
    ["file_extension"],
)

FILE_UPLOAD_SIZE = Histogram("file_upload_size_bytes", "Size of uploaded files")

FILE_DOWNLOAD_SIZE = Histogram("file_download_size_bytes", "Size of downloaded files")

ERROR_COUNT = Counter("app_errors_total", "Total number of errors", ["status_code"])
