import logging
from app.models.shadowsocks_connections import ShadowsocksConnection
from app.db.base import engine
from app.core.fastapi import app

ShadowsocksConnection.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)