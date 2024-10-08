from fastapi import FastAPI

from src.pizza.routes.size import router as size_router
from src.pizza.routes.dough_type import router as dough_type_router
from src.pizza.routes.category import router as category_router
from src.pizza.routes.pizza import router as pizza_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов API
    """
    app.include_router(size_router)
    app.include_router(dough_type_router)
    app.include_router(category_router)
    app.include_router(pizza_router)

    return app
