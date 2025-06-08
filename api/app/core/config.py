import logging
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    '''
    Settings class for the application.
    '''

    DATABASE_URL: str = os.getenv("DATABASE_URL", default="sqlite:///./data/shadowsocks.db")

    API_TITLE: str = "Shadowsocks Manager"

    ROOT_PATH: str = "/"
    
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", default="admin")

settings = Settings()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')