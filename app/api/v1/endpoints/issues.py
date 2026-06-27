from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("")
async def list_issues(user: User = Depends(get_current_user)):
    # TODO: implement issues module (see file map in README)
    return {"module": "issues", "status": "stub", "user": str(user.id)}
