import os
import signal
import subprocess
import json

def start_shadowsocks_connection(config: dict) -> int:
    """Запуск Shadowsocks сервера"""
    port = config["server_port"]
    password = config["password"]

    cmd = [
        "ss-server",
        "-s", "0.0.0.0",
        "-p", str(port),
        "-k", password,
        "-m", config["method"],
        "--plugin", config["plugin"],
        "--plugin-opts", config["plugin_opts"],
        "-t", str(config["timeout"]),
        "-u",  # для UDP поддержки
        "-v"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    return proc.pid

def stop_shadowsocks_connection(pid: int):
    """Остановка Shadowsocks сервера"""
    
    os.kill(pid, signal.SIGTERM)