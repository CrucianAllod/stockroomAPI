from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.order import OrderOrm, OrderItem, OrderStatus
from db.database import new_session
from models.product import ProductOrm
from schemas.order import Order as OrderSchemas, OrderCreate


class OrderRepository:
    @classmethod
    async def add_order(cls, order: OrderCreate) -> int:
        async with new_session() as session:
            data = order.model_dump()
            items_data = data.pop('items')
            
            for item_data in items_data:
                product_id = item_data['product_id']
                quantity_requested = item_data['quantity']
                
                product_query = select(ProductOrm).filter(ProductOrm.id == product_id)
                product_result = await session.execute(product_query)
                product = product_result.scalars().first()
                
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
                
                if product.quantity < quantity_requested:
                    raise HTTPException(status_code=400, detail=f"Not enough quantity for product ID {product_id}")
            
            new_order = OrderOrm(**data)
            session.add(new_order)
            await session.flush()

            for item_data in items_data:
                item = OrderItem(**item_data, order_id=new_order.id)
                session.add(item)
                product.quantity -= item_data['quantity']

            await session.commit()
            return new_order.id

    @classmethod
    async def get_orders(cls) -> list[OrderSchemas]:
        async with new_session() as session:
            query = select(OrderOrm).options(selectinload(OrderOrm.items))
            result = await session.execute(query)
            order_models = result.scalars().all()
            orders = [OrderSchemas.model_validate(order_model) for order_model in order_models]
            return orders
        
    @classmethod
    async def get_order(cls, order_id: int) -> OrderSchemas:
        async with new_session() as session:
            query = select(OrderOrm).filter(OrderOrm.id == order_id).options(selectinload(OrderOrm.items))
            result = await session.execute(query)
            order_model = result.scalars().first()
            return OrderSchemas.model_validate(order_model)
        
    @classmethod
    async def update_order(cls, order_id: int, status: OrderStatus) -> OrderSchemas:
        async with new_session() as session:
            query = select(OrderOrm).filter(OrderOrm.id == order_id).options(selectinload(OrderOrm.items))
            result = await session.execute(query)
            order_model = result.scalars().first()
            if order_model:
                order_model.status = status
                await session.commit()
                await session.refresh(order_model)
                return OrderSchemas.model_validate(order_model)
            return None
    
    @classmethod
    async def delete_order(cls, order_id: int):
        async with new_session() as session:
            query = select(OrderOrm).filter(OrderOrm.id == order_id)
            result = await session.execute(query)
            order_model = result.scalars().first()
            if order_model:
                await session.delete(order_model)
                await session.commit()
                return OrderSchemas.model_validate(order_model)
            return None           
