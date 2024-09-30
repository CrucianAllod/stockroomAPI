from sqlalchemy import select
from models.product import ProductOrm
from db.database import new_session
from schemas.product import Product as ProductSchemas, ProductCreate


class ProductRepository:
    @classmethod
    async def add_product(cls, product: ProductCreate) -> int:
        async with new_session() as session:
            data = product.model_dump()
            new_product = ProductOrm(**data)
            session.add(new_product)
            await session.flush()
            await session.commit()
            return new_product.id

    @classmethod
    async def get_products(cls) -> list[ProductSchemas]:
        async with new_session() as session:
            query = select(ProductOrm)
            result = await session.execute(query)
            product_models = result.scalars().all()
            products = [ProductSchemas.model_validate(product_model) for product_model in product_models]
            return products
        
    @classmethod
    async def get_product(cls, product_id: int) -> ProductSchemas:
        async with new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            return ProductSchemas.model_validate(product_model) if product_model else None
        
    @classmethod
    async def update_product(cls, product_id: int, product: ProductCreate) -> ProductSchemas:
        async with new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            if product_model:
                for key, value in product.model_dump().items():
                    setattr(product_model, key, value)
                await session.commit()
                await session.refresh(product_model)
                return ProductSchemas.model_validate(product_model)
            return None
    
    @classmethod
    async def delete_product(cls, product_id: int):
        async with new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            if product_model:
                await session.delete(product_model)
                await session.commit()
                return ProductSchemas.model_validate(product_model)
            return None           
