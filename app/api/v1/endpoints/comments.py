from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("")
async def list_comments(user: User = Depends(get_current_user)):
    # TODO: implement comments module (see file map in README)
    return {"module": "comments", "status": "stub", "user": str(user.id)}
