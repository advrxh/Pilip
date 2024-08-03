from datetime import datetime
from enum import Enum
from typing import Optional

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.base import PydanticModel
from pydantic import Field


class Status(str, Enum):
    open = "open"
    closed = "closed"
    scheduled = "scheduled"


class EventORM(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, null=False)
    prompt = fields.CharField(max_length=300, null=False)
    additional_info = fields.TextField(null=True)
    thumbnail = fields.CharField(max_length=100, null=True)
    start_time = fields.DatetimeField(auto_now_add=True, null=False)
    end_time = fields.DatetimeField(null=False)

    class Meta:
        table = "events"


class Event(PydanticModel):
    id: int = Field()
    title: str = Field(max_length=100)
    prompt: str = Field(max_length=300)
    additional_info: Optional[str] = Field(default=None)
    thumbnail: Optional[str] = Field(max_length=100, default=None)
    start_time: Optional[datetime] = Field(default=datetime.utcnow())
    end_time: datetime = Field()


class EventInput(PydanticModel):
    title: str = Field(max_length=100)
    prompt: str = Field(max_length=300)
    additional_info: Optional[str] = Field(default=None)
    thumbnail: Optional[str] = Field(max_length=100, default=None)
    start_time: Optional[datetime] = Field(default=datetime.utcnow())
    end_time: datetime = Field()


class EventStatusORM(Model):
    id = fields.IntField(pk=True)
    status = fields.CharEnumField(Status, default=Status.scheduled)

    class Meta:
        table = "events_status"


class EventStatus(PydanticModel):
    id: int = Field()
    status: Optional[Status] = Field(default=Status.scheduled)
