import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user, require_role
from app.models.user import User
from app.models.enums import Role
from app.schemas.organization import (
    OrgCreate, OrgOut, MemberAdd, MemberOut, TeamCreate, TeamOut,
)
from app.crud import organization as org_crud

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrgOut, status_code=201)
async def create_organization(
    data: OrgCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await org_crud.create_org(db, name=data.name, slug=data.slug, owner_id=user.id)


@router.get("", response_model=list[OrgOut])
async def my_organizations(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await org_crud.list_user_orgs(db, user.id)


@router.post("/{org_id}/members", response_model=MemberOut, status_code=201)
async def add_member(
    org_id: uuid.UUID, data: MemberAdd,
    _=Depends(require_role(Role.admin, Role.manager)), db: AsyncSession = Depends(get_db),
):
    return await org_crud.add_member(db, org_id=org_id, user_id=data.user_id, role=data.role)


@router.post("/{org_id}/teams", response_model=TeamOut, status_code=201)
async def create_team(
    org_id: uuid.UUID, data: TeamCreate,
    _=Depends(require_role(Role.admin, Role.manager)), db: AsyncSession = Depends(get_db),
):
    return await org_crud.create_team(db, org_id=org_id, name=data.name)


@router.get("/{org_id}/teams", response_model=list[TeamOut])
async def list_teams(
    org_id: uuid.UUID, _=Depends(require_role()), db: AsyncSession = Depends(get_db),
):
    return await org_crud.list_teams(db, org_id)
