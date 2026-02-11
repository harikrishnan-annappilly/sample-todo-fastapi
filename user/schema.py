from sqlmodel import SQLModel, Field, select
from datetime import datetime
from db import get_session
from typing import Optional


class PasswordInput(SQLModel):
    password: str = Field(nullable=False)


class UserInput(PasswordInput):
    username: str = Field(nullable=False, unique=True)


class UserModel(UserInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    def save(self):
        with get_session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        with get_session() as session:
            session.delete(self)
            session.commit()

    @classmethod
    def find_one(cls, **kwargs):
        with get_session() as session:
            return session.exec(select(cls).filter_by(**kwargs)).first()

    @classmethod
    def find_all(cls):
        with get_session() as session:
            return session.exec(select(cls)).all()
