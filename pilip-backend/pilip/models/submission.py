from typing import Dict, List

from pydantic import Field, BaseModel


class Submission(BaseModel):
    file_id: int = Field()  # file_id
    post_id: int = Field()  # post_id
