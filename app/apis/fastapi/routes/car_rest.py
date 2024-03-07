
from http import HTTPStatus
from app.businesses.cars_bo import CarsBusiness
from app.cdi import Injector
from app.commons.fields import ObjectIdStr
from app.dtos.cars_schema import CarsCreateRequest, CarsCreateResponse, CarsResponse, SearchCarsParams, UpdateCarRequest
from fastapi import (  # noqa
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
    Response,
)

router = APIRouter(prefix="/api/v1/cars", tags=["cars"])

cars_bo = Injector.auto_wired(CarsBusiness)

@router.get(
    "",
    summary="Lista cars",
    response_model=list[CarsResponse],
)
async def search(
    params: SearchCarsParams = Depends()
):
    """
    Retorna lista de carros
    """
    return await cars_bo.search_cars(params)


@router.post(
    "",
    summary="Cria Cars",
    response_model=CarsCreateResponse,
    status_code=HTTPStatus.CREATED,
)
async def create(body: CarsCreateRequest):
    """
    Cria um registro de carro
    """
    return await cars_bo.create_car(body)


@router.get(
    "/{car_id}",
    summary="",
    response_model=CarsResponse,
)
async def get_by_id(
    car_id: ObjectIdStr,
):
    """
    Busca e retorna carro por ID
    """
    return await cars_bo.get_car_by_id_or_fail(car_id)


@router.delete(
    "/{car_id}",
    summary="",
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete(car_id: ObjectIdStr):
    """
    Deleta carro
    """
    return await cars_bo.delete_car(car_id)


@router.put(
    "/{car_id}",
    summary="",

)
async def update(
    car_id: ObjectIdStr,
    body: UpdateCarRequest,
):
    """
    Atualiza dados de carro
    """
    if await cars_bo.update_car(car_id, body):
        return Response(status_code=HTTPStatus.OK)