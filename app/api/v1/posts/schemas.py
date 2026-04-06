

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    title: str
    content: str
    # tag: Optional[List[str]] = None
    # user: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
