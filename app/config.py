from pydantic import BaseModel
from functools import lru_cache
from dotenv import load_dotenv
import os

# 确保加载 .env 文件
load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:ckb518pk@localhost/disasterdb")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 