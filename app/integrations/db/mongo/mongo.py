from typing import TYPE_CHECKING

from motor.motor_asyncio import AsyncIOMotorClient

if TYPE_CHECKING:
    from motor.core import AgnosticCollection, AgnosticDatabase


class Mongo:
    def __init__(self, dsn: str):
        self._client = AsyncIOMotorClient(dsn, tz_aware=True)
        self._db = self._client.get_default_database()

    @property
    def database(self) -> "AgnosticDatabase":
        return self._db
    
    @property
    def cars(self) -> "AgnosticCollection":
        return self.database.cars

    async def ping(self):
        return await self._client.admin.command({"ping": 1})

    async def startup(self):
        try:
            await self.ping()
        except Exception as e:
            # Não impede a aplicação de iniciar pois normalmente fica no
            # processo de retentativas de conexão.
            ...

    def shutdown(self):
        if self._client:
            self._client.close()
