from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("")
async def list_activity(user: User = Depends(get_current_user)):
    # TODO: implement activity module (see file map in README)
    return {"module": "activity", "status": "stub", "user": str(user.id)}
