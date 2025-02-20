import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import main_router
from app.core import settings, exc
from app.core.exc import handlers


def _include_router(app: FastAPI) -> None:
    app.include_router(main_router.router)


def _add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _add_handlers(app: FastAPI) -> None:
    app.add_exception_handler(exc.NotAuthorizedException, handlers.handle_not_authorized_exception)
    app.add_exception_handler(exc.ObjectAlreadyExistsException, handlers.handle_object_already_exists)
    app.add_exception_handler(exc.ObjectNotFoundException, handlers.handle_object_not_found)
    app.add_exception_handler(exc.ForbiddenException, handlers.handle_forbidden_exception)
    app.add_exception_handler(exc.BadRequestException, handlers.handle_bad_request_exception)


def create_app() -> FastAPI:
    app = FastAPI()

    _include_router(app)
    _add_middleware(app)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
