from typing import TYPE_CHECKING

from fastapi.middleware.cors import CORSMiddleware

if TYPE_CHECKING:
    from fastapi import FastAPI

    from app.utils import Settings


def configure_cors(app: "FastAPI", settings: "Settings") -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
