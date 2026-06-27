from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, oauth, organizations, projects, issues, comments,
    notifications, search, analytics, activity, admin,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(organizations.router)
api_router.include_router(projects.router)
api_router.include_router(issues.router)
api_router.include_router(comments.router)
api_router.include_router(notifications.router)
api_router.include_router(search.router)
api_router.include_router(analytics.router)
api_router.include_router(activity.router)
api_router.include_router(admin.router)
