
import pytest
from http import HTTPStatus
from app.cdi import Injector

from app.repositories.cars_repository import CarsRepository

BASE_URL = "/api/v1/cars"

car_repository = Injector.auto_wired(CarsRepository)

@pytest.mark.asyncio
class TestCar:
    @pytest.fixture()
    async def clear_db(self):
        await car_repository._collection.delete_many({})

    async def test_should_create_car(self,clear_db, client):
        payload = {
            "name": "Uno teste",
            "brand": "Fiat",
            "detail": {
                "year": "2010",
                "color": "cinza"
            }
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == HTTPStatus.CREATED


    async def test_should_get_cars(self,clear_db, client):
        payload = {
            "name": "Uno teste",
            "brand": "Fiat",
            "detail": {
                "year": "2010",
                "color": "cinza"
            }
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == HTTPStatus.CREATED

        response = await client.get(BASE_URL)
        assert response.status_code == HTTPStatus.OK

        assert response.json()[0]["name"] == payload["name"]


    async def test_should_get_car(self,clear_db, client):
        payload = {
            "name": "Uno teste",
            "brand": "Fiat",
            "detail": {
                "year": "2010",
                "color": "cinza"
            }
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == HTTPStatus.CREATED

        car_id = response.json()["id"]

        response = await client.get(f"{BASE_URL}/{car_id}")
        assert response.status_code == HTTPStatus.OK

        assert response.json()["name"] == payload["name"]


    async def test_should_delete_car(self,clear_db, client):
        payload = {
            "name": "Uno teste",
            "brand": "Fiat",
            "detail": {
                "year": "2010",
                "color": "cinza"
            }
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == HTTPStatus.CREATED

        car_id = response.json()["id"]

        response = await client.delete(f"{BASE_URL}/{car_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT


    async def test_should_put_car(self,clear_db, client):
        payload = {
            "name": "Uno teste",
            "brand": "Fiat",
            "detail": {
                "year": "2010",
                "color": "cinza"
            }
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == HTTPStatus.CREATED

        car_id = response.json()["id"]

        payload["detail"]["year"] = 2011

        response = await client.put(f"{BASE_URL}/{car_id}", json=payload)
        assert response.status_code == HTTPStatus.OK


        response = await client.get(f"{BASE_URL}/{car_id}")

        assert response.json()["detail"]["year"] == 2011