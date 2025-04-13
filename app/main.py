from fastapi import FastAPI
from app.controllers import shadowsocks_api
from app.models.shadowsocks_connections import ShadowsocksConnection
from app.database import engine

ShadowsocksConnection.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(shadowsocks_api.router)