import abc

from initcommerce.common.value_object import ID
from pydantic import BaseConfig, BaseModel, Field, validator


class BaseEntity(BaseModel, metaclass=abc.ABCMeta):
    id: int = Field(default_factory=ID.fetch_one)

    class Config(BaseConfig):
        orm_mode = True


__all__ = [
    BaseEntity,
    Field,
    validator,
]
