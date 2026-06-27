from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def list_notifications(user: User = Depends(get_current_user)):
    # TODO: implement notifications module (see file map in README)
    return {"module": "notifications", "status": "stub", "user": str(user.id)}
