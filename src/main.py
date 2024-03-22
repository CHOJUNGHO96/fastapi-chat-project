# coding=utf-8
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

from config import conf
from container import Container
from infrastructure.db.mongo import MongoDB
from middleware import dispatch_middlewares
from presentation import router

templates = Jinja2Templates(directory="templates")
container = Container()
config = conf()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    mongodb: MongoDB = container.mongo()
    await mongodb.connect()
    yield
    await mongodb.close()


def create_app(_config) -> FastAPI:
    _app = FastAPI(title=_config.PROJECT_NAME, lifespan=lifespan)

    _app.container = container

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=("GET", "POST", "PUT", "DELETE"),
        allow_headers=["*"],
    )

    _app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=dispatch_middlewares)

    _app.include_router(router, prefix="/api/v1")

    def game_credit_openapi():
        if _app.openapi_schema:
            return _app.openapi_schema
        openapi_schema = get_openapi(
            title="cjh_chat",
            version=_config.VERSION,
            routes=_app.routes,
        )
        _app.openapi_schema = openapi_schema
        return _app.openapi_schema

    _app.openapi = game_credit_openapi

    return _app


app = create_app(config)

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.164.1", port=8080, reload=True, access_log=False)
