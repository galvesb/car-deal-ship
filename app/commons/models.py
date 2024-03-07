from datetime import datetime

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int = Field(1, description="Número da página", ge=1)
    per_page: int = Field(
        10,
        description="Quantidade de itens a retornar por página",
        ge=1,
        le=20,
    )

    class Config:
        abstract = True
        schema_extra = {"example": {"page": 1, "per_page": 20}}
