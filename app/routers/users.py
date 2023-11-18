from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from app.auth import get_current_active_user
from app.dependencies import require_role
from app.schemas import User
from app.crud import fetch_all

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_role("admin"))],
    responses={404: {"description": "Not found"}},
)

@router.get("/users/", tags=["users"])
async def read_users():
    users = fetch_all('users', 'username')
    return users

@router.get("/users/me", tags=["users"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
