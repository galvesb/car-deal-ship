from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return ObjectId(value if isinstance(value, str) else str(value))
        except Exception as e:
            raise ValueError("Not a valid ObjectId") from e
