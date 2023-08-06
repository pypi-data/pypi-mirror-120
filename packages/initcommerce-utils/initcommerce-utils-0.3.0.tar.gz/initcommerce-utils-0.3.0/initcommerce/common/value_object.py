from datetime import datetime
from enum import Enum

from initcommerce.common.uuid import UUID as ID
from pydantic import BaseModel, Field


class StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)


class CreateTimeStampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateTimeStampMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


__all__ = [
    "ID",
]
