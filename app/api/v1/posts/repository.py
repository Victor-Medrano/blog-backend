

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import PostORM


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, post_id: int) -> Optional[PostORM]:
        post_find = select(PostORM).where(PostORM.id == post_id)
        return self.db.execute(post_find).scalar_one_or_none()

    def get_by_slug(self, slug: str) -> Optional[PostORM]:
        query = (select(PostORM).where(PostORM.slug == slug))
        return self.db.execute(query).scalar_one_or_none()

    # search

    def create_post(self, title: str, content: str) -> PostORM:

        post = PostORM(title=title, content=content)
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    # update
    # delete
