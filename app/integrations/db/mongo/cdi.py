from app.cdi import Module, Provider
from app.utils import Settings

from .mongo import Mongo


class MongoProvider(Provider[Mongo]):
    __slots__ = ("_settings",)

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get(self) -> Mongo:
        return Mongo(self._settings.db_dsn)


class MongoModule(Module):
    def configure(self) -> None:
        self.bind_singleton(Mongo, to_provider=MongoProvider)
