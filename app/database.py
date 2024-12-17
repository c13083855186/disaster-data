# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# 创建会话本地类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 使用新的 declarative_base
Base = declarative_base()

