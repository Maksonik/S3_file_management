from fastapi import FastAPI
from prometheus_client import make_asgi_app

from sfm.core.routers import app_routes

app = FastAPI()

app.include_router(app_routes)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
