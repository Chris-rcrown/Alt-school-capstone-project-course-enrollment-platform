from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.schemas.user import UserRead

router = APIRouter()


@router.get(
    "/me",
    response_model=UserRead,
    tags=["General"],
    summary="Get current user profile",
    description="Return the authenticated user's profile. Available to both admins and students.",
)
def read_current_user(current_user=Depends(get_current_active_user)):
    return current_user
