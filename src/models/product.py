from sqlalchemy.orm import Mapped, mapped_column
from db.database import Model



class ProductOrm(Model):
    __tablename__ = 'products'
    
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(default=None)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)