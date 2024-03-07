from fastapi import FastAPI

from app.cdi import Injector


def create_app() -> FastAPI:
    Injector.startup()

    return Injector.inject(FastAPI)
