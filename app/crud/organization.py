import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization, OrganizationMember, Team
from app.models.enums import Role


async def create_org(db: AsyncSession, *, name: str, slug: str, owner_id: uuid.UUID) -> Organization:
    org = Organization(name=name, slug=slug, owner_id=owner_id)
    db.add(org)
    await db.flush()
    db.add(OrganizationMember(organization_id=org.id, user_id=owner_id, role=Role.admin))
    await db.flush()
    return org


async def list_user_orgs(db: AsyncSession, user_id: uuid.UUID) -> list[Organization]:
    res = await db.execute(
        select(Organization).join(OrganizationMember)
        .where(OrganizationMember.user_id == user_id)
    )
    return list(res.scalars().all())


async def add_member(db: AsyncSession, *, org_id: uuid.UUID, user_id: uuid.UUID, role: Role) -> OrganizationMember:
    m = OrganizationMember(organization_id=org_id, user_id=user_id, role=role)
    db.add(m)
    await db.flush()
    return m


async def create_team(db: AsyncSession, *, org_id: uuid.UUID, name: str) -> Team:
    t = Team(organization_id=org_id, name=name)
    db.add(t)
    await db.flush()
    return t


async def list_teams(db: AsyncSession, org_id: uuid.UUID) -> list[Team]:
    res = await db.execute(select(Team).where(Team.organization_id == org_id))
    return list(res.scalars().all())
