from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field, SecretStr, validator  # noqa

from app.domains.base import ExternalReference  # noqa


class Examples:

    __slots__ = ()

    timestamp = datetime.fromtimestamp(1645480001.059086, tz=timezone.utc)
    object_id = "620ffd3409259bb79824d146"
    user_id = "5453a818-9085-498f-ac45-8e5989ddbda2"
    uuid_v4 = "303940f9-92f6-459d-9141-53675a70b6fc"
    seller_id = "mmadeira"
