from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("")
async def list_admin(user: User = Depends(get_current_user)):
    # TODO: implement admin module (see file map in README)
    return {"module": "admin", "status": "stub", "user": str(user.id)}
