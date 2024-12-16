from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.bloq import Bloq

router = APIRouter(
    prefix="/bloqs",
    tags=["bloqs"]
)

@router.get("/", response_model=List[Bloq])
async def get_bloqs(session: AsyncSession = Depends(get_session)):
    bloqs = await session.execute(select(Bloq))
    return bloqs.scalars().all()

@router.get("/{bloq_id}", response_model=Bloq)
async def get_bloq(bloq_id: str, session: AsyncSession = Depends(get_session)):
    bloq = await session.get(Bloq, bloq_id)
    if not bloq:
        raise HTTPException(status_code=404, detail="Bloq not found")
    return bloq

@router.post("/", response_model=Bloq)
async def create_bloq(bloq: Bloq, session: AsyncSession = Depends(get_session)):
    session.add(bloq)
    await session.commit()
    await session.refresh(bloq)
    return bloq 