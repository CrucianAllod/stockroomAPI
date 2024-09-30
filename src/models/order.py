from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Model
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, TIMESTAMP
import enum



class OrderStatus(enum.Enum):
    IN_PROCESS = "in process"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class OrderOrm(Model):
    __tablename__ = 'orders'
    
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[OrderStatus] = mapped_column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.IN_PROCESS)
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
class OrderItem(Model):
    __tablename__ = 'order_items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    order = relationship("OrderOrm", back_populates="items")
    product = relationship("ProductOrm")