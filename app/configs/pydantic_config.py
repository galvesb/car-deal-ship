from typing import Any, Callable, Type

import pydantic
from bson import ObjectId


def _register_encoder(object_type: Type[Any], encoder: Callable[[Any], Any]):
    pydantic.json.ENCODERS_BY_TYPE[object_type] = encoder


def configure_pydantic():
    _register_encoder(ObjectId, str)
