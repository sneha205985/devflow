from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import get_db
from app.crud import user as user_crud
from app.core.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth/google", tags=["auth"])
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def google_login(request):
    return await oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@router.get("/callback")
async def google_callback(request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    info = token.get("userinfo")
    user = await user_crud.get_by_email(db, info["email"])
    if not user:
        user = await user_crud.create_user(
            db, email=info["email"], full_name=info.get("name", info["email"]),
            password=None, oauth_provider="google", is_verified=True,
        )
    redirect = (
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?access_token={create_access_token(user.id)}"
        f"&refresh_token={create_refresh_token(user.id)}"
    )
    return RedirectResponse(redirect)
