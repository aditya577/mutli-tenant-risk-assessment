from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.api.routes import router as risk_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Risk Assessment Service (POC)",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(risk_router)
