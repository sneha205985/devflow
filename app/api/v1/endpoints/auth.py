from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, Token, RefreshRequest
from app.crud import user as user_crud
from app.core.security import (
    verify_password, create_access_token, create_refresh_token,
    create_email_token, decode_token, hash_password,
)
from app.api.deps import get_current_user
from app.models.user import User
from app.workers.tasks import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    if await user_crud.get_by_email(db, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = await user_crud.create_user(
        db, email=data.email, full_name=data.full_name, password=data.password
    )
    token = create_email_token(user.id)
    send_verification_email.delay(user.email, token)
    return user


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db, form.username)
    if not user or not user.hashed_password or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=Token)
async def refresh(data: RefreshRequest):
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
    sub = payload["sub"]
    return Token(
        access_token=create_access_token(sub),
        refresh_token=create_refresh_token(sub),
    )


@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "email":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")
    import uuid
    user = await db.get(User, uuid.UUID(payload["sub"]))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    user.is_verified = True
    return {"detail": "Email verified"}


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return user
