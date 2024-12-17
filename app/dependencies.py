# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import verify_access_token
from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    user = payload.get("sub")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未认证的用户")
    return user

# 添加数据库依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
