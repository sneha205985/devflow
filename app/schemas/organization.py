import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import Role


class OrgCreate(BaseModel):
    name: str
    slug: str


class OrgOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    slug: str
    owner_id: uuid.UUID
    created_at: datetime


class MemberAdd(BaseModel):
    user_id: uuid.UUID
    role: Role = Role.viewer


class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    role: Role


class TeamCreate(BaseModel):
    name: str


class TeamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    organization_id: uuid.UUID
