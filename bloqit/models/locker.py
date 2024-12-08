import uuid
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

from .bloq import Bloq

class LockerStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class Locker(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    bloqId: str = Field(foreign_key="bloq.id")
    status: LockerStatus
    isOccupied: bool = Field(default=False)
    
    bloq: Bloq = Relationship(back_populates="lockers")
    rents: list["Rent"] = Relationship(back_populates="locker")