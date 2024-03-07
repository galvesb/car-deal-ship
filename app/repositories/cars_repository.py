from typing import TYPE_CHECKING, List, Optional, Union
from app.domains.cars_domain import Cars
from app.dtos.cars_schema import SearchCarsParams, UpdateCarRequest
from ..commons.fields import ObjectIdStr
from ..utils.pagination import calc_skips
from .base import (
    Mongo,
    ObjectId,
    WriteConcernMajority,
    as_object_id,
    from_dict_to_mongo,
    from_model_to_mongo,
    from_mongo_list_to_model_list,
    from_mongo_to_model,
)


class CarsRepository:
    if TYPE_CHECKING:
        from motor.core import AgnosticCollection

        _collection: AgnosticCollection

    def __init__(self, mongo: Mongo):
        self._collection = mongo.cars.with_options(
            write_concern=WriteConcernMajority
        )

    async def search(self, filters: SearchCarsParams) -> List[Cars]:
        skips = calc_skips(filters.per_page, filters.page)
        query = {}

        if name := filters.name:
            query["name"] = name

        if year := filters.year:
            query["detail.year"] = year
        

        cars_data = await self._collection.find(
            query, skip=skips, limit=filters.per_page
        ).to_list(None)
        return from_mongo_list_to_model_list(cars_data, Cars)
    
    async def create(self, car) -> ObjectIdStr:
        insert_result = await self._collection.insert_one(
            from_model_to_mongo(car)
        )
        return insert_result.inserted_id
    
    async def get_by_id(self, car_id: Union[str, ObjectId]) -> Optional[Cars]:
        if car_data := await self._collection.find_one(
            {"_id": as_object_id(car_id)}
        ):
            return from_mongo_to_model(car_data, Cars)

        return None
    
    async def delete_car(self, car_id: Union[str, ObjectId]) -> bool:
        deleted_result = await self._collection.delete_one(
            {"_id": as_object_id(car_id)}
        )
        return deleted_result.deleted_count == 1
    
    async def update_car_data(
        self,
        car_id: Union[str, ObjectId],
        body: UpdateCarRequest,
    ):
        update_data = {
            **body.dict(exclude_none=True),
        }

        query = {"_id": as_object_id(car_id)}
        update_set = {"$set": from_dict_to_mongo(update_data)}

        print(f"query {query}")

        print(f"update_set {update_set}")

        return await self._collection.update_one(query, update_set)