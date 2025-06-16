# S3 File Management

S3 File Management is a FastAPI application for working with files stored in an Amazon S3 bucket. The service provides endpoints to upload, list and delete files as well as generate temporary download links. It also includes a simple rate limiter and an asynchronous in-memory cache used by the S3 client.

## Project structure

```
./sfm               - main application package
├── apps            - feature specific modules
│   ├── files       - API for file operations
│   └── internal    - health check endpoints
└── core            - application core
    ├── integrations - S3 integration layer
    ├── permissions  - rate limiter implementation
    ├── settings.py  - configuration management
    ├── main.py      - FastAPI application factory
    └── routers.py   - API router setup

```

Unit tests are stored in the `tests/` directory. They use `pytest` and record AWS requests with `pytest-vcr`.

## Requirements

* Python 3.12+
* Access to an AWS S3 bucket

The application dependencies are managed via [Poetry](https://python-poetry.org/).
Install them by running:

```bash
poetry install
```

Alternatively you can install the project using `pip`:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root based on `env.template`:

```
S3_BUCKET_NAME="your-bucket-name"
ALLOWED_FILE_TYPES=["jpg", "png", "pdf"]

# AMAZON credentials
AMAZON_ACCESS_KEY_ID=...
AMAZON_SECRET_ACCESS_KEY=...
AMAZON_REGION_NAME="eu-north-1"
```

The `ALLOWED_FILE_TYPES` list controls which file extensions are accepted during upload.

## Running the application

Use `uvicorn` to start the service:

```bash
uvicorn sfm.core.main:app --reload
```

The API will be available at `http://localhost:8000`. The OpenAPI documentation is provided at `/docs`.

### Main endpoints

* `GET  /v1/files/{prefix}` – list files within the given S3 prefix. Supports `max_keys` and `recursive` query parameters.
* `GET  /v1/files/{prefix}/{filename}/download` – generate a pre‑signed download URL.
* `POST /v1/files/{prefix}` – upload a file to the specified prefix.
* `DELETE /v1/files/{prefix}/{filename}` – delete a file from the bucket.
* `GET  /v1/healthcheck` – service availability check.

The file operations are rate limited to **20 requests per minute** per client IP. Exceeding this limit results in an HTTP 429 error.

## Testing

To run the unit tests use:

```bash
pytest
```

The tests rely on recorded VCR cassettes and require the development dependencies specified in `pyproject.toml`.
