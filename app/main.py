from fastapi import FastAPI
from .internal import admin
from .routers import api, items, users, auth

app = FastAPI()

app.include_router(api.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "PostgresNavigator API: Entry point"}