import uuid
from sqlmodel import SQLModel, Field, Relationship


class Bloq(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    title: str
    address: str 

    lockers: list["Locker"] = Relationship(back_populates="bloq")
    