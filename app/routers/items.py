from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header
import app.crud as crud

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    items = crud.fetch_all('items', 'name')
    return items

@router.get("/{item_id}")
async def read_item(item_id: str):
    item = crud.fetch_one('items', 'id', item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": item["name"], "item_id": item['id']}

