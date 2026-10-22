from fastapi import FastAPI

from src.api import health
from src.config.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(health.router)
