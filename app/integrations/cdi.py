from app.cdi import Module


class IntegrationModule(Module):
    def configure(self) -> None:
        from .db.mongo.cdi import MongoModule

        self.install(MongoModule())
