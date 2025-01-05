from fastapi import FastAPI
from uvicorn import run
from my_service.depends.service_container import ServiceContainer
from my_service.routers.router import router
from uvicorn import run
# from core.settings import settings
# from my_service.db.base_db import base_db
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    container = ServiceContainer()

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
    application.include_router(router)
    return application


app = create_app()


if __name__ == "__main__":
    run('main:app', host="0.0.0.0", port=7005, reload=True)