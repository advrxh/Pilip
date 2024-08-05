from pydantic import BaseModel
from pydantic.fields import Field


class Auth(BaseModel):
    username: str = Field()
    password: str = Field()
