from importlib import resources

from fastapi import FastAPI

from app.cdi import Module, Provider
from app.configs import configure_pydantic
from app.integrations import Mongo
from app.utils import Settings

from .configs import (
    configure_cors,
    configure_exception_handlers,
    configure_request_hooks,
)


def configure_routes(app: FastAPI):
    from .routes.health_rest import router as health_router
    from .routes.car_rest import router as car_router

    routes = (health_router, car_router)

    for router in routes:
        app.include_router(router)


class FastAPIProvider(Provider[FastAPI]):
    __slots__ = ("_settings", "_mongo")

    def __init__(self, settings: Settings, mongo: Mongo) -> None:
        self._settings = settings
        self._mongo = mongo

    def get(self) -> FastAPI:
        settings = self._settings
        description_md = resources.read_text(
            __package__, "openapi_description.md"
        )
        app = FastAPI(
            title=settings.title,
            description=description_md,
            version=settings.version,
            openapi_tags=[
                {
                    "name": "healthcheck",
                    "description": "Serviços utilitários para verificar status"
                    " do ambiente",
                },
                {
                    "name": "Cars",
                    "description": "Crie, altere, remova e publique Carros"
                },
            ],
            openapi_url=settings.openapi_path,
            on_startup=[self._mongo.startup],
            on_shutdown=[self._mongo.shutdown],
        )

        configure_pydantic()
        configure_cors(app, settings)
        configure_exception_handlers(app)
        configure_request_hooks(app, settings)
        configure_routes(app)

        return app


class FastAPIModule(Module):
    def configure(self) -> None:
        self.bind_singleton(FastAPI, to_provider=FastAPIProvider)
