from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import HTTPException


class ApplicationException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        message: str = None,
    ):
        super().__init__(status_code, detail=detail, headers=headers)

        self.code = code
        self.message = message


class UnauthorizedException(ApplicationException):
    def __init__(
        self,
        code: int = HTTPStatus.UNAUTHORIZED,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(HTTPStatus.UNAUTHORIZED, code, detail, headers)


class ForbiddenException(ApplicationException):
    def __init__(
        self,
        code: int = HTTPStatus.FORBIDDEN,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(HTTPStatus.FORBIDDEN, code, detail, headers)


class NotFoundException(ApplicationException):
    def __init__(
        self,
        code: int = HTTPStatus.NOT_FOUND,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(HTTPStatus.NOT_FOUND, code, detail, headers)


class UnprocessableEntityException(ApplicationException):
    def __init__(
        self,
        code: int = HTTPStatus.UNPROCESSABLE_ENTITY,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        message: str = None,
    ):
        super().__init__(
            HTTPStatus.UNPROCESSABLE_ENTITY, code, detail, headers, message
        )


class ConflictException(ApplicationException):
    def __init__(
        self,
        code: int = HTTPStatus.CONFLICT,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        message: str = None,
    ):
        super().__init__(HTTPStatus.CONFLICT, code, detail, headers, message)


class GenericException(ApplicationException):
    def __init__(
        self,
        status_code: int,
        code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        message: str = None,
    ):
        super().__init__(status_code, code, detail, headers, message)
