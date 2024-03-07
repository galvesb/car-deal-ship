from http import HTTPStatus

import pytest

from app.apis.fastapi.routes.health_rest import router
from app.utils.constants import APP_VERSION

BASE_URL = router.prefix
pytestmark = [pytest.mark.asyncio]


async def test_should_health_check_with_ping(client):
    res = await client.get(BASE_URL)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"pong": True, "version": APP_VERSION}


async def test_should_get_api_version(client):
    res = await client.get(f"{BASE_URL}/version")

    assert res.status_code == HTTPStatus.OK
    assert res.text == f'"{APP_VERSION}"'
