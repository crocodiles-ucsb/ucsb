from fastapi import FastAPI

from .api import auth


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth.router, tags=['auth'])
    return app
