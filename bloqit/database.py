from sqlmodel import SQLModel, Session, create_engine
import os

DATABASE_NAME= os.getenv("DATABASE_NAME", "bloqit")
DATABASE_USER= os.getenv("DATABASE_USER", "bloqit")
DATABASE_PASSWORD= os.getenv("DATABASE_PASSWORD", "mypassword")
DATABASE_HOST= os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT= os.getenv("DATABASE_PORT", "5432")

engine = create_engine(
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session 