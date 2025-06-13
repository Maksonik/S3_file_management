from fastapi import FastAPI

from sfm.core.routers import app_routes

app = FastAPI()

app.include_router(app_routes)
