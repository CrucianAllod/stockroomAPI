from fastapi import APIRouter, HTTPException, Depends
from models.order import OrderStatus
from schemas.order import Order, OrderCreate
from repositories.order import OrderRepository


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate, repository: OrderRepository = Depends()):
    order_id = await repository.add_order(order)
    return await repository.get_order(order_id)

@router.get("/", response_model=list[Order])
async def read_orders(repository: OrderRepository = Depends()):
    return await repository.get_orders()

@router.get("/{order_id}", response_model= Order)
async def read_order(order_id: int, repository: OrderRepository = Depends()):
    order = await repository.get_order(order_id)
    if not order:
        return HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}/status", response_model= Order)
async def update_order(order_id: int, status: OrderStatus, repository: OrderRepository = Depends()):
    update_order = await repository.update_order(order_id, status)
    if not update_order:
        return HTTPException(status_code=404, detail="Order not found")
    return update_order 

@router.delete("/{order_id}", response_model= Order)
async def delete_order(order_id: int, repository: OrderRepository = Depends()):
    success = await repository.delete_order(order_id)
    if not success:
        return HTTPException(status_code=404, detail="Order not found")
    return success 
        