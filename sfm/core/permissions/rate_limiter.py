from collections import defaultdict
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from sfm.core.constants import TOO_MANY_REQUESTS_MESSAGE

_request_logs: dict[str, list[datetime]] = defaultdict(list)

RATE_LIMIT = 20
WINDOW_SECONDS = 60


async def check_rate_limit(request: Request) -> None:
    """
    Check if the current client (by IP address) has exceeded the allowed request rate.

    This function enforces a simple in-memory rate limit per IP address, using a fixed time window.

    :param request: The incoming HTTP request, used to extract the client's IP address.
    :return: None. Raises HTTPException with status 429 if the limit is exceeded.
    """
    ip = request.client.host
    now = datetime.now(tz=UTC)

    recent = [ts for ts in _request_logs[ip] if now - ts < timedelta(seconds=WINDOW_SECONDS)]
    _request_logs[ip] = recent

    if len(recent) >= RATE_LIMIT:
        raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail=TOO_MANY_REQUESTS_MESSAGE)

    _request_logs[ip].append(now)
