# app/routers/auth.py (o el path donde está este archivo)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserOut, LoginRequest, Token
from app.security import get_password_hash, verify_password, create_access_token
from app.database import get_db
from app import crud
import os  # 👈 NUEVO

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # 👇 Rechazar si email ya existe
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 👇 SOLO si se quiere registrar como psicólogo: exigir invite_code
    if payload.role == "psychologist":
        expected = os.getenv("ADMIN_INVITE_CODE", "")
        if (not expected) or (payload.invite_code != expected):
            raise HTTPException(status_code=403, detail="Invite code required")

    # 👇 Crear usuario como antes
    user = crud.create_user(
        db,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
    )
    return user

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(subject=user.email)
    return {"access_token": token}
