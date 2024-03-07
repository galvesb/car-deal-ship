from .base import BaseModel, Field


class HealthResponse(BaseModel):
    pong: bool = Field(
        ...,
        title="Boolean value informing the success case. Always comes `true`",
    )
    version: str = Field(title="The API version")

    class Config:
        schema_extra = {"example": {"pong": True, "version": "0.0.1"}}
