import logging
from fastapi import FastAPI
from app.endpoints import shadowsocks
from app.models.shadowsocks_connections import ShadowsocksConnection
from app.db.base import engine
from app.core.config import settings

ShadowsocksConnection.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.API_TITLE)

app.include_router(shadowsocks.router)