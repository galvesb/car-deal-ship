import asyncio
from os.path import dirname, join

import pytest
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import AsyncClient

from app.cdi import Injector
from app.utils.settings import EnvironmentEnum, Settings


def pytest_generate_tests(metafunc):
    dotenv_path = join(dirname(__file__), ".test.env")
    load_dotenv(dotenv_path, override=True)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()

    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="session")
async def test_app(event_loop):
    from api_main import create_app

    app = create_app()

    async with LifespanManager(app):
        # TODO: Check db name

        yield app


@pytest.fixture
async def client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client



@pytest.fixture(autouse=True)
def test_environment():
    settings = Injector.inject(Settings)

    assert settings.env.is_test(), (
        f"Wrong environment: expected APP_ENV={EnvironmentEnum.TEST}, "
        f"got APP_ENV={settings.env}."
    )
