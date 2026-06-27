import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, *, email: str, full_name: str,
                      password: str | None, oauth_provider: str | None = None,
                      is_verified: bool = False) -> User:
    user = User(
        email=email, full_name=full_name,
        hashed_password=hash_password(password) if password else None,
        oauth_provider=oauth_provider, is_verified=is_verified,
    )
    db.add(user)
    await db.flush()
    return user
