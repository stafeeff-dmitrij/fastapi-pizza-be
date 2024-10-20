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
    description="Добавление (увеличение кол-ва) пиццы с выбранным типом теста и размером",
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


@router.delete(
    '/cart/{record_id}',
    name="Удаление пиццы из корзины",
    description="Удаление позиции товара из корзины / уменьшение товара на 1 в корзине",
    response_model=CartSchema | None,
    responses={
        status.HTTP_200_OK: {'model': CartSchema | None}
    },
)
async def delete_cart(
    record_id: int,
    one_record: bool = False,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление товара из корзины
    """

    record = await CartService.delete_cart(record_id=record_id, one_record=one_record, session=session)

    return record


@router.delete(
    '/cart',
    name="Очистка корзины",
    description="Удаление всех товаров из корзины",
    response_model=None,
    responses={
        status.HTTP_200_OK: {'model': None}
    },
)
async def clear_cart(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Очистка корзины
    """

    await CartRepository.clear(session=session)
