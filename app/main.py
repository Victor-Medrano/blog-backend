from dotenv import load_dotenv
from fastapi import FastAPI, Path, Query

from app.core.db import Base, engine
from app.api.v1.posts.router import router as post_router

app = FastAPI(title="Blog")

load_dotenv()


# BLOG_POST = [
#     {"id": 1, "title": "fastApi", "content": "Fastapi es un framework moderno"},
#     {"id": 2, "title": "django", "content": "Django es un monolito"},
#     {"id": 3, "title": "python",
#         "content": "Python es un lenguage de programacion mas usado"},
#     {"id": 4, "title": "golang", "content": "Golang es muy rapido"},
#     {"id": 5, "title": "gin", "content": "Gin es un framework de golang"},
#     {"id": 6, "title": "sql", "content": "Lenguaje universal de base de datos"},
#     {"id": 7, "title": "postgres", "content": "Es un entorno de base de datos"},
#     {"id": 8, "title": "docker", "content": "Maquina virtual de linux"},
#     {"id": 9, "title": "contenedores", "content": "Contiene la imagen de docker"},
#     {"id": 10, "title": "docker Compose",
#         "content": "Inicializa el contenedor y la imagen con un comando"}
# ]


# @app.get("/")
# def home():
#     return {"Message": "Bienvenidos"}


# @app.get("/posts")
# def list_posts(query: str | None = Query(default=None, description="Para buscar por titulo")):

#     if query:
#         result = [post for post in BLOG_POST if query.lower()
#                   in post["title"].lower()]

#         return {"data": result}

#     return {"data": BLOG_POST}


# @app.get("/posts/{post_id}")
# def get_post(post_id: int):

#     for post in BLOG_POST:
#         if post["id"] == post_id:
#             return {"data": post}

#     return {"error": "Post no encontrado"}


def create_app() -> FastAPI:
    app = FastAPI(title="Blog")

    Base.metadata.create_all(bind=engine)  # dev

    app.include_router(post_router)

    return app


app = create_app()
