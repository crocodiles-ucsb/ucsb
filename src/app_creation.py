import uvicorn
from fastapi import FastAPI

from src.database.database import Base
from src.api import auth
from src.api import admins
from src.api import index


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth.router, tags=['auth'])
    app.include_router(admins.router, tags=['admins'],prefix='/admins')
    app.include_router(index.router, tags=['index'])
    return app


if __name__ == '__main__':
    Base.metadata.create_all()
    uvicorn.run(create_app())