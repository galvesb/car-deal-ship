from typing import List, Type, TypeVar, Union

from bson import ObjectId
from pydantic import BaseModel
from pymongo import WriteConcern

from app.integrations import Mongo  # noqa
from app.utils.pagination import calc_skips  # noqa

T = TypeVar("T")

WriteConcernMajority = WriteConcern(w="majority")


def _from_mongo_to_pydantic(attr: str) -> str:
    if attr == "_id":
        return "id"
    return attr


def _mongo_fields_to_pydantic(data: Type[T]) -> T:
    if isinstance(data, (list, set, tuple)):
        return type(data)([_mongo_fields_to_pydantic(item) for item in data])
    elif isinstance(data, dict):
        return {
            _from_mongo_to_pydantic(attr): _mongo_fields_to_pydantic(value)
            for attr, value in data.items()
        }
    return data


def _from_pydantic_to_mongo(attr: str) -> str:
    if attr == "id":
        return "_id"
    return attr


def _pydantic_fields_to_mongo(data: Type[T]) -> T:
    if isinstance(data, (list, set, tuple)):
        return type(data)([_pydantic_fields_to_mongo(item) for item in data])
    elif isinstance(data, dict):
        return {
            _from_pydantic_to_mongo(attr): _pydantic_fields_to_mongo(value)
            for attr, value in data.items()
            if not (attr == "id" and value is None)
        }

    return data


def from_mongo_to_model(data: dict, model: Type[T]) -> T:
    return model(**_mongo_fields_to_pydantic(data))


def from_dict_to_mongo(model: dict) -> dict:
    return _pydantic_fields_to_mongo(model)


def from_model_to_mongo(model: BaseModel, exclude_none: bool = False) -> dict:
    return from_dict_to_mongo(model.dict(exclude_none=exclude_none))


def from_mongo_list_to_model_list(data: List, model: Type[T]) -> List[T]:
    return [from_mongo_to_model(current_data, model) for current_data in data]


def as_object_id(value: Union[ObjectId, str]) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    return ObjectId(value)
