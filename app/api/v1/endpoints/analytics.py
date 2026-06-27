from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
async def list_analytics(user: User = Depends(get_current_user)):
    # TODO: implement analytics module (see file map in README)
    return {"module": "analytics", "status": "stub", "user": str(user.id)}
