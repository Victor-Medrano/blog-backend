
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class PostORM(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("title", name="unique_post_title"),)

    id: Mapped[int] = mapped_column(
        Integer, index=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
