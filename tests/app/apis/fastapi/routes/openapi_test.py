from http import HTTPStatus

import pytest

pytestmark = [pytest.mark.asyncio]


async def test_should_generate_openapi(client):
    res = await client.get("/openapi.json")

    assert res.status_code == HTTPStatus.OK
