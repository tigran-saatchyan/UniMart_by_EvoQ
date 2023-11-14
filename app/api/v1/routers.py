from app.api.v1.products import router as product_router
from app.api.v1.users import router as user_router

all_routers = [
    product_router,
    user_router,
]
