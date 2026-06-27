import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.models.organization import OrganizationMember
from app.models.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise cred_exc
    user_id = payload.get("sub")
    if not user_id:
        raise cred_exc
    user = await db.get(User, uuid.UUID(user_id))
    if not user or not user.is_active:
        raise cred_exc
    return user


def require_role(*allowed: Role):
    """Org-scoped RBAC guard. Expects org_id path param."""
    async def _dep(
        org_id: uuid.UUID,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> OrganizationMember:
        res = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.user_id == user.id,
            )
        )
        member = res.scalar_one_or_none()
        if not member:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not an org member")
        if allowed and member.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient role")
        return member
    return _dep
