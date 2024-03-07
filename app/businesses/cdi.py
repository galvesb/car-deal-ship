from app.cdi import Module


class BusinessModule(Module):
    def configure(self) -> None:
        from .cars_bo import CarsBusiness

        self.bind_singleton(CarsBusiness)
