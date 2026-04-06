

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.posts.repository import PostRepository
from app.api.v1.posts.schemas import PostBase, PostCreate
from app.core.db import get_db
from app.models.post import PostORM


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/{post_id}", response_model=PostBase, response_description="Post encontrado")
def get_post(post_id: int, db: Session = Depends(get_db)):

    repository = PostRepository(db)
    post = repository.get(post_id=post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    return post


@router.post("", response_model=PostBase, response_description="Post creado (OK)", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostORM:
    repository = PostRepository(db)
    try:
        post = repository.create_post(
            title=post.title,
            content=post.content
        )

        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el post")
