from sqlmodel import create_engine, Session
from contextlib import contextmanager

DATABASE_URI = "sqlite:///data.db"

engine = create_engine(DATABASE_URI, echo=True)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
