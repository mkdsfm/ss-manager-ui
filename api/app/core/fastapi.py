from fastapi import FastAPI
from app.endpoints import shadowsocks
from app.core.config import settings

app = FastAPI(title=settings.API_TITLE, root_path=settings.ROOT_PATH)

app.include_router(shadowsocks.router)