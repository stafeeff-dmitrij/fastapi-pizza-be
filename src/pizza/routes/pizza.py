from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.pizza.repositories.pizza import PizzaRepository
from src.pizza.schemas.pizza import PizzaSchema
from src.router import BaseRouter


router = BaseRouter(tags=['Пиццы'])

@router.get(
    '/pizzas',
    name="Возврат пицц",
    description="Возврат всех пицц с возможностью фильтрации по названию и пагинацией",
    response_model=list[PizzaSchema],
    responses={
        status.HTTP_200_OK: {'model': list[PizzaSchema]}
    },
)
async def get_pizzas(
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    limit: int = 6,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат пицц
    """

    pizzas = await PizzaRepository.get_list(
        name=name,
        category_id=category_id,
        limit=limit,
        offset=offset,
        session=session
    )

    return pizzas
