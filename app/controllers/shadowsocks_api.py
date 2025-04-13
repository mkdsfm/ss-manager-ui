from fastapi import APIRouter, Depends, Query
from app.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.shadowsocks_connections import ShadowsocksConnection
from fastapi.responses import JSONResponse
from fastapi import status

from app.shadowsocks_process_manager.manager import start_shadowsocks_connection, stop_shadowsocks_connection

router = APIRouter(prefix="/shadowsocks", tags=["Shadowsocks"])

@router.get("/{port}")
def get_by_port(port: int ,  db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    existing_connection = db.query(ShadowsocksConnection).filter(ShadowsocksConnection.server_port == port).first()

    return existing_connection

@router.get("all")
def all(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    existing_connection = db.query(ShadowsocksConnection).all()
    
    return existing_connection

@router.post("/{port}", status_code=status.HTTP_201_CREATED)
def create(port: int , db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    
    # Проверка, существует ли уже подключение на этом порту
    existing_connection = db.query(ShadowsocksConnection).filter(ShadowsocksConnection.server_port == port).first()
    if existing_connection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Connection already exists on this port")
    
    # Добавляем запись в базу данных
    new_connection = ShadowsocksConnection(
        server_port=port,
        password="password",
        method="chacha20-ietf-poly1305",
        plugin = "obfs-server",
        plugin_opts="obfs=http;failover=204.79.197.200:80",
        status="pending",
        enable=True
    )
    db.add(new_connection)
    db.commit()

    # Конфиг для Shadowsocks
    config = {
        "server": ["0.0.0.0"],
        "mode": "tcp_and_udp",
        "server_port": port,
        "password": "password",  # TODO вынести
        "timeout": 60,
        "method": "chacha20-ietf-poly1305", # TODO вынести
        "plugin": "obfs-server", # TODO вынести
        "plugin_opts": "obfs=http;failover=204.79.197.200:80" # TODO вынести
    }

    try:
        pid = start_shadowsocks_connection(config)
    except Exception as ex:
        new_connection.status = "failed" # TODO вынести в enum
        new_connection.error = ex
        db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Shadowsocks connection exception {ex}")
    
    # TODO добавить проверку статуса
    new_connection.status = "running"
    new_connection.pid = pid
    db.commit()

    return {"message": "Shadowsocks connection created", "config": config}

@router.patch("/{port}/enable")
def enable(port: int, enable: bool, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    connection = db.query(ShadowsocksConnection).filter(ShadowsocksConnection.server_port == port).first()
    if not connection:
        raise HTTPException(status_code=400, detail="Connection not found")
    
    config = {
        "server": ["0.0.0.0"],
        "mode": "tcp_and_udp",
        "server_port": port,
        "password": "password",  # TODO вынести
        "timeout": 60,
        "method": "chacha20-ietf-poly1305", # TODO вынести
        "plugin": "obfs-server", # TODO вынести
        "plugin_opts": "obfs=http;failover=204.79.197.200:80" # TODO вынести
    }


    if enable:
        try:
            pid = start_shadowsocks_connection(config)
        except Exception as ex:
            connection.status = "failed" # TODO вынести в enum
            connection.error = ex
            db.commit()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Shadowsocks connection exception {ex}")
        
        connection.status = "running"
        connection.pid = pid
        db.commit()
    else:
        try:
            stop_shadowsocks_connection(connection.pid)
        except ProcessLookupError:
            pass  # Процесс уже завершён
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to stop process: {e}")
        connection.status = "stopped"
        connection.enable = False
        connection.pid = None
        db.commit()


@router.delete("/{port}")
def delete(port: int , db: Session = Depends(get_db), user: str = Depends(get_current_user)):

    connection = db.query(ShadowsocksConnection).filter(ShadowsocksConnection.server_port == port).first()
    if not connection or not connection.pid:
        raise HTTPException(status_code=400, detail="Connection not found or PID missing")
    
    try:
        stop_shadowsocks_connection(connection.pid)
    except ProcessLookupError:
        pass  # Процесс уже завершён
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop process: {e}")
    
    if connection:
        db.delete(connection)
        db.commit()

    return {"message": f"Connection on port {port} deleted"}