import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_create_order(ac: AsyncClient):
    order_data = {
        "created_date": "2024-09-29T21:59:13.438Z",
        "status": "IN_PROCESS"
    }
    response = await ac.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == order_data["status"]

@pytest.mark.asyncio
async def test_read_orders(ac: AsyncClient):
    response = await ac.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_read_order(ac: AsyncClient):
    order_data = {
        "created_date": "2024-09-29T21:59:13.438Z",
        "status": "IN_PROCESS"
    }
    response = await ac.post("/orders/", json=order_data)
    order_id = response.json()["id"]

    response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == order_data["status"]

@pytest.mark.asyncio
async def test_update_order(ac: AsyncClient):
    order_data = {
        "created_date": "2024-09-29T21:59:13.438Z",
        "status": "IN_PROCESS"
    }
    response = await ac.post("/orders/", json=order_data)
    order_id = response.json()["id"]

    update_data = {"status": "SHIPPED"}
    response = await ac.put(f"/orders/{order_id}/status", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == update_data["status"]

@pytest.mark.asyncio
async def test_delete_order(ac: AsyncClient):
    order_data = {
        "created_date": "2024-09-29T21:59:13.438Z",
        "status": "IN_PROCESS"
    }
    response = await ac.post("/orders/", json=order_data)
    order_id = response.json()["id"]

    response = await ac.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id

    response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 404