from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.cart.repositories import CartRepository
from src.cart.schemas import CartSchema, PizzaAddToCartSchema
from src.cart.services import CartService
from src.database import get_async_session
from src.router import BaseRouter


router = BaseRouter(tags=['Корзина'])


@router.get(
    '/cart',
    name="Возврат корзины",
    description="Возврат всех товаров в корзине",
    response_model=list[CartSchema],
    responses={
        status.HTTP_200_OK: {'model': list[CartSchema]}
    },
)
async def get_cart(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат корзины с товарами
    """

    cart_records = await CartRepository.get_list(session=session)

    return cart_records


@router.post(
    '/cart',
    name="Добавление пиццы в корзину",
    description="Добавление одной пиццы с выбранным типом теста и размером",
    response_model=CartSchema,
    responses={
        status.HTTP_200_OK: {'model': CartSchema}
    },
)
async def add_pizza(
    data: PizzaAddToCartSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Добавление пиццы в корзину
    """

    record = await CartService.add_product(data=data, session=session)

    return record

