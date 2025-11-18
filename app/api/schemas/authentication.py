from typing import Annotated

from fastapi import Header
from pydantic import BaseModel, field_validator, Field


class UserLogin(BaseModel):
    username: str
    password: str

MINIMUM_APP_VERSION = "0.0.2"

class CommonHeaders(BaseModel):
    user_agent: str = Field(alias='User-Agent')
    accept_language: str = Field(alias='Accept-Language')


    # @field_validator('x_current_version')
    # def check_x_current_version(cls, value):
    #     if value < MINIMUM_APP_VERSION:
    #         raise ValueError('Требуется обновить приложение')
    #     return value

    @classmethod
    def from_headers(
            cls,
            user_agent: Annotated[str, Header(alias='User-Agent')],
            accept_language: Annotated[str, Header(alias='Accept-Language')],
    ):
        return cls(user_agent=user_agent, accept_language=accept_language)