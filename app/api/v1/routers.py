from app.api.v1.cart import router as cart_router
from app.api.v1.products import router as product_router

all_routers = [
    product_router,
    cart_router,
]
