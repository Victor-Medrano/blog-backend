

from typing import Literal, Optional, List

from pydantic import BaseModel, ConfigDict


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


class PaginatePost(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
    order_by: Literal["id", "title"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[PostBase]
