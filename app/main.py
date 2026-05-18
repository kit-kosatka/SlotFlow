from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.specialist import router as specialists_router
from app.api.routers.slots import router as slots_router
from app.api.routers.appointments import router as appointments_router
from app.db.base import engine, Base
from app import models
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="SlotFlow", version="1.0.0", lifespan=lifespan)


app.include_router(auth_router)
app.include_router(specialists_router)
app.include_router(slots_router)
app.include_router(appointments_router)
