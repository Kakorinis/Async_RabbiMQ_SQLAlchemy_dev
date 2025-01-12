from typing import List, Type

from fastapi import FastAPI
from uvicorn import run
from fastapi import APIRouter
from users_service.depends import UserServiceContainer
from authentication_service.depends import AuthServiceContainer
from authentication_service.routers import auth_router
from users_service.routers import user_router
from dependency_injector import containers

# from core.settings import settings
# from my_service.db.base_db import base_db
# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware


def create_app(depends_container: Type[containers.DeclarativeContainer], routers: List[APIRouter]) -> FastAPI:
    container = depends_container()

    # db = container.db()
    # db.create_database()

    # FastAPI и Starlette реализуют OPTIONS поддержку, но в запросах должны быть установлены оба заголовка Origin и Access-Control-Request-Method
    # https://github.com/fastapi/fastapi/issues/1849
    # origins = ["http://newstyle.ru:8092"]
    # middleware = [
    #     Middleware(
    #         CORSMiddleware,
    #         allow_origins=["*"],  # origins если [*], то в чем смысл защиты?
    #         allow_credentials=True,
    #         allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #         allow_headers=['X-CSRF-Token', 'X-Requested-With', 'Accept', 'Accept-Version', 'Content-Length',
    #                        'Content-MD5', 'Content-Type', 'Date', 'X-Api-Version', 'Authorization']
    #     )
    # ]

    # application = FastAPI(middleware=middleware)
    application = FastAPI()
    application.container = container
    for router in routers:
        application.include_router(router)
    return application


app = create_app(depends_container=UserServiceContainer, routers=[user_router])
app_2 = create_app(depends_container=AuthServiceContainer, routers=[auth_router])

if __name__ == "__main__":
    run('main:app', host="0.0.0.0", port=7005, reload=True)
    run('main:app_2', host="0.0.0.0", port=7007, reload=True)
