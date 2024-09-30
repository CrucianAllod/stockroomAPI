import pytest
from httpx import AsyncClient

from db.database import new_session
from models.product import ProductOrm


@pytest.mark.asyncio
async def test_create_product(ac: AsyncClient):
    product_data = {"name": "Test Product", "description": "A test product", "price": 9.99, "quantity": 10}
    response = await ac.post("/products/", json=product_data)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200



    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["quantity"] == product_data["quantity"]


@pytest.mark.asyncio
async def test_read_products(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_read_product(ac: AsyncClient):
    product_data = {"name": "Test Product", "description": "A test product", "price": 9.99}
    async with new_session() as session:
        new_product = ProductOrm(**product_data)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        product_id = new_product.id

    response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]


@pytest.mark.asyncio
async def test_update_product(ac: AsyncClient):
    product_data = {"name": "Test Product", "description": "A test product", "price": 9.99}
    updated_data = {"name": "Updated Product", "description": "An updated product", "price": 19.99}

    async with new_session() as session:
        new_product = ProductOrm(**product_data)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        product_id = new_product.id

    response = await ac.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]
    assert data["price"] == updated_data["price"]


@pytest.mark.asyncio
async def test_delete_product(ac: AsyncClient):
    product_data = {"name": "Test Product", "description": "A test product", "price": 9.99}

    async with new_session() as session:
        new_product = ProductOrm(**product_data)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        product_id = new_product.id

    response = await ac.delete(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]

    response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 404