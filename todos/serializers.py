from .enums import Status
from pydantic import BaseModel
from datetime import datetime


class TodoSerializer(BaseModel):
    id: str
    title: str
    description: str
    status: Status
    responsible: str
    due_date: datetime

    class Config:
        orm_mode = True


class TodoCreateSerializer(BaseModel):
    title: str
    description: str
    status: Status
    responsible: str
    due_date: datetime


class TodoUpdateSerializer(TodoCreateSerializer):
    pass
