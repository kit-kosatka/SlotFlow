from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.db.base import engine, Base
from app import models

app = FastAPI(title="SlotFlow", version="1.0.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)