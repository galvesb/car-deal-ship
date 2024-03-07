from http import HTTPStatus

import pytest

from app.commons.exceptions import (
    GenericException,
    UnprocessableEntityException,
)

BASE_URL = "/api/v1/health"
pytestmark = [pytest.mark.asyncio]


async def test_should_handle_python_exception(client, mocker):
    mocker.patch(
        "app.utils.settings.Settings.version",
        mocker.PropertyMock(side_effect=Exception),
    )

    with pytest.raises(Exception):
        await client.get(BASE_URL)


async def test_should_handle_generic_exception(client, mocker):
    exc = GenericException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        code=1005,
        detail="Detail",
        message="Message",
    )

    mocker.patch(
        "app.utils.settings.Settings.version",
        mocker.PropertyMock(side_effect=exc),
    )

    res = await client.get(BASE_URL)

    assert res.status_code == exc.status_code
    assert res.json() == {
        "code": exc.code,
        "detail": exc.detail,
        "message": exc.message,
    }


async def test_should_handle_validation_exception(client, mocker):
    exc = UnprocessableEntityException(code=2000, detail="Detail")

    mocker.patch(
        "app.utils.settings.Settings.version",
        mocker.PropertyMock(side_effect=exc),
    )

    res = await client.get(BASE_URL)

    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert res.json() == {
        "code": exc.code,
        "detail": exc.detail,
        "message": None,
    }
