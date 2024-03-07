from app.commons.fields import ObjectIdStr
from app.commons.models import BaseModel, Field



class Detail(BaseModel):
    year: int = Field(None)
    color: str = Field(None)

class BaseCars(BaseModel):
    name: str = Field(title="Nome do carro", example="Lojas Exemplo LTDA")
    brand: str = Field(title="marca")
    detail: Detail | None = Field(None, title="")


class Cars(BaseCars):
    id: ObjectIdStr | None = Field(None, title="Identificador do Carro")