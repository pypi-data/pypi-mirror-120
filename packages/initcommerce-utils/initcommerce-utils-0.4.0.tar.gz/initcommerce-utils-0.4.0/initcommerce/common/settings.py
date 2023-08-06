from pydantic import BaseSettings as PydanticSettings
from pydantic import validator


class BaseSettings(PydanticSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


__all__ = [
    validator,
]
