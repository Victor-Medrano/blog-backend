

from math import ceil
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.posts.repository import PostRepository
from app.api.v1.posts.schemas import PaginatePost, PostBase, PostCreate, PostUpdate
from app.core.db import get_db
from app.models.post import PostORM


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginatePost)
def list_post(
    query: Optional[str] = Query(
        default=None,
        description="Texto para buscar el titulo",
        # alias="search",
        min_length=3,
        max_length=50,
        pattern=r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$"
    ),
    page: int = Query(
        1,
        description="Numero de paginas (>=1)",
        ge=1,
        le=50
    ),
    per_page: int = Query(
        5,
        description="Numero de resultados (1-50)",
        ge=5,
        le=50
    ),
    order_by: Literal["id", "title"] = Query(
        "id",
        description="Ordenalos por id o por titulo"
    ),
    direction: Literal["asc", "desc"] = Query(
        "asc",
        description="Ordena de manera ascendente o decendente"
    ),
    db: Session = Depends(get_db)

):
    repository = PostRepository(db)

    total, items = repository.search(
        query=query,
        page=page,
        per_page=per_page,
        order_by=order_by,
        direction=direction
    )

    total_pages = ceil(total/per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(page, total_pages)

    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages > 0 else False

    return PaginatePost(
        total=total,
        total_pages=total_pages,
        page=current_page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev,
        direction=direction,
        order_by=order_by,
        search=query,
        items=items
    )


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


@router.put("/{post_id}", response_model=PostBase, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):

    respository = PostRepository(db)
    post = respository.get(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    try:
        update = data.model_dump(exclude_unset=True)
        post = respository.update_post(post, update)

        db.commit()
        db.refresh(post)
        return post

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Error al actualizar el post")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    repository = PostRepository(db)

    post = repository.get(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    try:
        repository.delete_post(post)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Error al eliminar el post")
