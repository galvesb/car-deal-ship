from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.commons.exceptions import (
    ConflictException,
    ForbiddenException,
    GenericException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
)

if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response


async def _handle_request_validation_exception(
    request: "Request", exc: RequestValidationError
) -> "Response":
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "code": HTTPStatus.UNPROCESSABLE_ENTITY,
                "message": "Erro de validação",
            }
        ),
    )


async def _handle_unauthorized_exception(
    request: "Request", exc: UnauthorizedException
) -> "Response":
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "detail": exc.detail,
                "code": exc.code,
                "message": "Erro de autorização",
            }
        ),
    )


async def _handle_forbidden_exception(
    request: "Request", exc: ForbiddenException
) -> "Response":
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "detail": exc.detail,
                "code": exc.code,
                "message": "Acesso negado",
            }
        ),
    )


async def _handle_not_found_exception(
    request: "Request", exc: NotFoundException
) -> "Response":
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "detail": exc.detail,
                "code": exc.code,
                "message": "Recurso não encontrado",
            }
        ),
    )


async def _handle_generic_exception(
    request: "Request", exc: GenericException
) -> "Response":
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "detail": exc.detail,
                "code": exc.code,
                "message": exc.message,
            }
        ),
    )


def _handle_python_exception(request: "Request", exc: Exception) -> "Response":
    return JSONResponse(
        status_code=getattr(
            exc, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR
        ),
        content=jsonable_encoder(
            {
                key: getattr(exc, key, None)
                for key in ("detail", "code", "message")
            }
        ),
    )


def configure_exception_handlers(app: "FastAPI") -> None:

    handlers = (
        (RequestValidationError, _handle_request_validation_exception),
        (UnauthorizedException, _handle_unauthorized_exception),
        (ForbiddenException, _handle_forbidden_exception),
        (NotFoundException, _handle_not_found_exception),
        (GenericException, _handle_generic_exception),
        (UnprocessableEntityException, _handle_generic_exception),
        (ConflictException, _handle_generic_exception),
        (Exception, _handle_python_exception),
    )

    for exception, handler in handlers:
        app.add_exception_handler(exception, handler)
