from fastapi import Depends, FastAPI

from .dependencies import require_role
from .internal import admin
from .routers import items, users, auth

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "PostgresNavigator API: Entry point"}