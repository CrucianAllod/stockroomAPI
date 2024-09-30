from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    
class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    class Config:
        from_attributes = True