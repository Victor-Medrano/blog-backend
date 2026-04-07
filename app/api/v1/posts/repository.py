

from math import ceil
from typing import List, Optional, Tuple

from sqlalchemy import func, select
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

    def search(
        self,
        query,
        order_by,
        direction,
        page,
        per_page
    ) -> Tuple[int, List[PostORM]]:

        results = select(PostORM)

        if query:
            query = results.where(PostORM.title.ilike(f"%{query}%"))

        total = self.db.scalar(
            select(func.count()).select_from(results.subquery())) or 0

        if total == 0:
            return 0, []

        current_page = min(page, max(1, ceil(total/per_page)))

        order_col = PostORM.id if order_by == "id" else func.lower(
            PostORM.title)

        results = results.order_by(
            order_col.asc() if direction == "asc" else order_col.desc())

        start = (current_page - 1) * per_page
        items = self.db.execute(results.limit(
            per_page).offset(start)).scalars().all()

        return total, items

    def create_post(self, title: str, content: str) -> PostORM:

        post = PostORM(title=title, content=content)
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def update_post(self, post: PostORM, update: dict) -> PostORM:
        for key, value in update.items():
            setattr(post, key, value)
        return post

    def delete_post(self, post: PostORM) -> None:
        self.db.delete(post)
