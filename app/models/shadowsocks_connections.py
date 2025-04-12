from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShadowsocksConnection(Base):
    __tablename__ = "shadowsocks_connections"

    id = Column(Integer, primary_key=True, index=True)
    server_port = Column(Integer, unique=True, index=True)
    password = Column(String)
    method = Column(String)
    plugin_opts = Column(String)
    status = Column(String)
    enable = Column(Boolean, default=False)
    error = Column(String, nullable=True)
    pid = Column(Integer, nullable=True)
