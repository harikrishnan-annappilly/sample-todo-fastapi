from sqlmodel import SQLModel, Field, select
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from db import get_session


class StatusEnum(str, Enum):
    todo = "Todo"
    in_progress = "In Progress"
    done = "Done"


class TaskEditInput(BaseModel):
    title: Optional[str] = None
    status: Optional[StatusEnum] = None


class TaskInput(SQLModel):
    title: str = Field(nullable=False)
    status: Optional[StatusEnum] = Field(nullable=False, default=StatusEnum.todo)


class TaskModel(TaskInput, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=datetime.now())

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
