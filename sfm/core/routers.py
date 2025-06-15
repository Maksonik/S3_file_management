from fastapi import APIRouter

from sfm.apps.files.views import files_api_v1
from sfm.apps.internal.views import internal_api_v1


def get_app_routes() -> APIRouter:
    """
    creates and returns an instance of APIRouter for applications
    :return: instance of APIRouter
    """
    app_api_v1 = APIRouter(prefix="/v1")
    app_api_v1.include_router(internal_api_v1)
    app_api_v1.include_router(files_api_v1)

    app_router = APIRouter()
    app_router.include_router(app_api_v1)

    return app_router


app_routes = get_app_routes()
