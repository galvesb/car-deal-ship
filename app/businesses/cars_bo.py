from typing import List
from app.commons.exceptions import NotFoundException, UnprocessableEntityException
from app.commons.fields import ObjectIdStr

from app.domains.cars_domain import Cars
from app.dtos.cars_schema import CarsCreateRequest, CarsCreateResponse, SearchCarsParams, UpdateCarRequest

from app.repositories import CarsRepository



class CarsBusiness:
    def __init__(
        self,
        car_repository: CarsRepository,
    ):
        self._car_repository = car_repository


    async def search_cars(
        self, params: SearchCarsParams
    ) -> List[Cars]:
        return await self._car_repository.search(params)
    

    async def create_car(
        self, data: CarsCreateRequest
    ) -> CarsCreateResponse:

        car = Cars(
            **data.dict(),
        )

        id_car = await self._car_repository.create(car)

        return CarsCreateResponse(id=id_car)
    

    async def get_car_by_id_or_fail(self, car_id) -> Cars:

        if car := await self._car_repository.get_by_id(car_id):
            return car

        raise NotFoundException(detail=f"Carro não encontrado com o id {car_id}")
    

    async def delete_car(self, car_id: ObjectIdStr) -> bool:
        car = await self.get_car_by_id_or_fail(car_id)

        return await self._car_repository.delete_car(car.id)
    
    async def update_car(
            self,car_id: ObjectIdStr, body: UpdateCarRequest
        ):
            car = await self.get_car_by_id_or_fail(car_id)

            update_result = await self._car_repository.update_car_data(
                car.id, body
            )

            if not update_result.modified_count:
                raise UnprocessableEntityException(
                    detail="Falha ao atualizar o carro"
                )
            return update_result
