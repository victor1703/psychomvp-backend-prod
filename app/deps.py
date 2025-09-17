from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
from app.config import settings
from app import models
from sqlalchemy import select

ALGORITHM = "HS256"
security = HTTPBearer()

DbDep = Annotated[Session, Depends(get_db)]
CredDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

def get_current_user(db: DbDep, creds: CredDep) -> models.User:
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        sub: str | None = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.execute(select(models.User).where(models.User.email == sub)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user
