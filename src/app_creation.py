from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import (
    admins,
    auth,
    contractors,
    files,
    index,
    operators,
    representatives,
    requests,
    securitites,
    workers,
)
from src.database.database import Base


def create_app() -> FastAPI:
    path = Path(__file__).resolve().parent / 'static'
    app = FastAPI()
    app.mount('/static', StaticFiles(directory=str(path)), name='static')
    app.include_router(auth.router, tags=['auth'])
    app.include_router(admins.router, tags=['admins'], prefix='/admins')
    app.include_router(index.router, tags=['index'])
    app.include_router(operators.router, tags=['operators'], prefix='/operators')
    app.include_router(securitites.router, tags=['securities'], prefix='/securities')
    app.include_router(contractors.router, tags=['contractors'], prefix='/contractors')
    app.include_router(files.router, tags=['files'], prefix='/files')
    app.include_router(
        representatives.router,
        tags=['representatives'],
        prefix='/contractor_representatives',
    )
    app.include_router(workers.router, tags=['workers'], prefix='/workers')
    app.include_router(requests.router, tags=['requests'], prefix='/requests')
    return app


if __name__ == '__main__':
    Base.metadata.create_all()
    uvicorn.run(create_app())
