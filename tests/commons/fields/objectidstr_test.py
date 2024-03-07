import pytest
from bson import ObjectId
from pydantic import BaseModel

from app.commons.fields import ObjectIdStr


class AnModel(BaseModel):
    value: ObjectIdStr


def test_should_raise_for_invalid_value():
    with pytest.raises(ValueError):
        AnModel(value="test")


def test_should_convert_string_to_objectid():
    obj = AnModel(value="555fc7956cda204928c9dbab")
    assert isinstance(obj.value, ObjectId)
