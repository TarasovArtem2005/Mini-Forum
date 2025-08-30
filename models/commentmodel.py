from pydantic import BaseModel
from typing import Optional


class CommmentCreate(BaseModel):
    post_id: Optional[str] = None
    post_title: Optional[str] = None
    content: str

