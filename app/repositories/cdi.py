from app.cdi import Module


class RepositoryModule(Module):
    def configure(self) -> None:
        from .cars_repository import CarsRepository

        self.bind_singleton(CarsRepository)
