from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def list_search(user: User = Depends(get_current_user)):
    # TODO: implement search module (see file map in README)
    return {"module": "search", "status": "stub", "user": str(user.id)}
