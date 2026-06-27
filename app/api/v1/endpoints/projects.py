from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def list_projects(user: User = Depends(get_current_user)):
    # TODO: implement projects module (see file map in README)
    return {"module": "projects", "status": "stub", "user": str(user.id)}
