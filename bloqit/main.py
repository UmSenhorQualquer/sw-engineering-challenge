from fastapi import FastAPI
from .data import load_json_data
import uvicorn

from .database import create_db_and_tables, engine
from .routers import bloqs, lockers, rents
from .models.bloq import Bloq
from .models.locker import Locker
from .models.rent import Rent
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    await load_json_data(engine)
    yield

app = FastAPI(
    title="Bloq API",
    description="A FastAPI service for managing lockers and parcel deliveries",
    version="0.1.0",
    lifespan=lifespan
)

# Include routers
app.include_router(bloqs.router)
app.include_router(lockers.router)
app.include_router(rents.router)


def start():
    """Entry point for the application."""
    uvicorn.run(
        "bloqit.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    start() 