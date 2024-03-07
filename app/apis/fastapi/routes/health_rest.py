from app.cdi import Injector
from app.dtos.health_schema import HealthResponse
from app.utils import Settings

from fastapi import (  # noqa
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
    Response,
)

settings = Injector.auto_wired(Settings)

router = APIRouter(prefix="/api/v1/health", tags=["healthcheck"])


@router.get(
    "",
    summary="Saúde da aplicação",
    response_model=HealthResponse,
    response_description="""No caso de resposta de sucesso da aplicação, você
    receberá a seguinte informação:
- `pong`: Valor boleano informando o caso de sucesso. Sempre vem `true`.
- `version`: A versão da API.""",
)
async def ping():
    """
    Com esta chamada de _ping_ você estará verificando:

    - Se a aplicação está respondendo/viva.
    - Batendo no banco de dados.
    """
    return {"pong": True, "version": settings.version}


@router.get(
    "/version",
    summary="String com a versão da aplicação",
    response_description="Retorna a versão da aplicação no formato de string",
)
async def get_version() -> str:
    """
    Versão da API
    """
    return settings.version
