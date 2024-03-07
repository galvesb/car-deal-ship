from app.commons.fields import ObjectIdStr
from app.commons.models import Pagination
from .base import BaseModel, Field


class Detail(BaseModel):
    year: int = Field(None)
    color: str = Field(None)


class BaseCars(BaseModel):
    name: str = Field(title="Nome do carro", example="Lojas Exemplo LTDA")
    brand: str = Field(title="marca")
    detail: Detail = Field(None, title="")


class CarsResponse(BaseCars):
    id: ObjectIdStr = Field(..., title="Identificador do Carro")


class SearchCarsParams(Pagination):
    name: str = Field(
        None, title=""
    )
    year: int = Field(
        None, title=""
    )

class CarsCreateResponse(BaseModel):
    id: ObjectIdStr = Field(
        ...,
        title="Identificador do carro",
    )


class CarsCreateRequest(BaseCars):
    id: ObjectIdStr | None = Field(
        None,
        title="Identificador do carro",
    )

class UpdateCarRequest(BaseCars):
    ...