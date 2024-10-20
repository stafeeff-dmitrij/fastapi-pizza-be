from fastapi import HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.cart.models import Cart
from src.cart.repositories import CartRepository
from src.cart.schemas import PizzaAddToCartSchema
from src.pizza.repositories.dough_type import DoughTypeRepository
from src.pizza.repositories.pizza import PizzaRepository
from src.pizza.repositories.size import SizeRepository


class CartService:
    """
    Добавление пиццы в корзину
    """

    @classmethod
    async def add_product(cls, data: PizzaAddToCartSchema, session: AsyncSession) -> Cart:
        """
        Добавление пиццы в корзину
        :param pizza: id пиццы, типа теста и размера пиццы
        :param session: объект асинхронной сессии
        :return: новая запись о пицце в корзине
        """

        record = await CartRepository.get(pizza_id=data.pizza_id, type_id=data.type_id, size_id=data.size_id, session=session)

        if record:
            if record.count == 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail='Нельзя добавить в корзину более 10 одинаковых пицц!'
                )

            logger.info('Пицца уже есть в корзине, увеличение кол-ва на 1')
            updated_record = await CartRepository.increment(record=record, session=session)

            return updated_record

        # Проверка и создание новой записи
        pizza = await PizzaRepository.get(pizza_id=data.pizza_id, session=session)

        if not pizza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Пицца не найдена'
            )

        dough_type = await DoughTypeRepository.get(dough_type_id=data.type_id, session=session)

        if not dough_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Некорректный тип теста'
            )

        size = await SizeRepository.get(size_id=data.size_id, session=session)

        if not size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Некорректный размер пиццы'
            )

        new_record = await CartRepository.create(pizza=pizza, type=dough_type, size=size, session=session)
        logger.info('Пицца добавлена в корзину')

        return new_record

    @classmethod
    async def delete(cls, record_id: int, session: AsyncSession) -> None:
        """
        Удаление товара из корзины
        :param record: запись для удаления
        :param session: объект асинхронной сессии
        :return: None
        """

        record = await CartRepository.get_for_id(record_id=record_id, session=session)

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена'
            )

        await CartRepository.delete(record=record, session=session)
