from typing import Annotated

from fastapi import Depends

from sfm.core.settings import Settings, get_settings

from .router import internal_api_v1


@internal_api_v1.get("/healthcheck")
async def get_healthcheck(settings: Annotated[Settings, Depends(get_settings)]) -> dict:
    """
    Return a non-empty response if the service works.
    """
    return {"status": "ok", "App name": settings.APP_NAME}
