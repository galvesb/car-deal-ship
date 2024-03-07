import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response

    from app.utils import Settings


def _now() -> float:
    return time.perf_counter()


class RequestHookMiddleware:
    __slots__ = ("_settings",)

    def __init__(self, settings: "Settings") -> None:
        self._settings = settings

    async def _after_request(
        self, request: "Request", response: "Response", request_start: float
    ) -> None:
        request_end = _now()

        if request.url.path:
            elapsed_time = (request_end - request_start) * 1000

        return response

    async def hook(self, request: "Request", call_next) -> "Response":
        request_start = _now()

        response = await call_next(request)

        await self._after_request(request, response, request_start)

        return response


def configure_request_hooks(fastapi: "FastAPI", settings: "Settings") -> None:

    request_hook = RequestHookMiddleware(settings)

    @fastapi.middleware("http")
    async def request_hooks(request: "Request", call_next):
        return await request_hook.hook(request, call_next)
