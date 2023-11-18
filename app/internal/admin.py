from fastapi import APIRouter
from fastapi import Depends
from ..dependencies import require_role

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
    responses={418: {"description": "Admin route"}},
)

@router.post("/")
async def update_admin():
    return {"message": "Admin update functionality"}
