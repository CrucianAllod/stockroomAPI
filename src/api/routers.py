from .product import router as products_router
from .order import router as orders_router

all_routers = [
   orders_router,
   products_router,
]
