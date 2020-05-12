from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import admins, auth, index, operators
from src.database.database import Base


def create_app() -> FastAPI:
    path = Path(__file__).resolve().parent / 'static'
    app = FastAPI()
    app.mount('/static', StaticFiles(directory=str(path)), name='static')
    app.include_router(auth.router, tags=['auth'])
    app.include_router(admins.router, tags=['admins'], prefix='/admins')
    app.include_router(index.router, tags=['index'])
    app.include_router(operators.router, tags=['operators'], prefix='/operators')
    return app


if __name__ == '__main__':
    Base.metadata.create_all()
    uvicorn.run(create_app())
