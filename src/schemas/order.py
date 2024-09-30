from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime, timezone
from models.order import OrderStatus
from .orderItem import OrderItemCreate, OrderItem


class OrderBase(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.IN_PROCESS
    
class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    created_date: Optional[datetime] = None
    
    @field_validator('created_date', mode='before')
    def set_created_date(cls, value):
        return value or datetime.now(timezone.utc)

class Order(OrderBase):
    id: int
    created_date: datetime
    items: List[OrderItem]
    
    class Config:
        from_attributes = True