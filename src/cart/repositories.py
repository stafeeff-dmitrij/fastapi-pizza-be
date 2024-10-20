from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.cart.models import Cart
from src.pizza.models import Pizza, PizzaDoughType, PizzaSize


class CartRepository:
    """
    Действия с корзиной с товарами
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> list[Cart]:
        """
        Возврат категорий пицц
        :param session: объект асинхронной сессии
        :return: список с категориями
        """
        query = select(Cart)
        cart_records = await session.execute(query)

        return cart_records.scalars().all()

    @classmethod
    async def get(cls, pizza_id: int, type_id: int, size_id: int, session: AsyncSession) -> Cart | None:
        """
        Поиск и возврат пиццы в корзине по id пиццы, теста и размера
        :param pizza_id: идентификатор пиццы
        :param type_id: идентификатор типа теста
        :param size_id: идентификатор размера пиццы
        :param session: объект асинхронной сессии
        :return: объект записи о пицце в корзине
        """
        query = select(Cart).where(Cart.pizza_id == pizza_id, Cart.type_id == type_id, Cart.size_id == size_id)
        record = await session.execute(query)

        return record.scalar_one_or_none()

    @classmethod
    async def get_for_id(cls, record_id: int, session: AsyncSession) -> Cart | None:
        """
        Поиск и возврат записи из корзины по id
        :param record_id: идентификатор записи
        :param session: объект асинхронной сессии
        :return: объект записи о пицце в корзине
        """
        query = select(Cart).where(Cart.id == record_id)
        record = await session.execute(query)

        return record.scalar_one_or_none()

    @classmethod
    async def create(cls, pizza: Pizza, type: PizzaDoughType, size: PizzaSize, session: AsyncSession) -> Cart:
        """
        Создание записи о новой пицце в корзине
        :param pizza: объект пиццы
        :param type: тип теста
        :param size: размер пиццы
        :param session: объект асинхронной сессии
        :return: новая запись о пицце в корзине
        """
        record = Cart(pizza=pizza, type=type, size=size)
        session.add(record)
        await session.commit()

        return record

    @classmethod
    async def increment(cls, record: Cart, session: AsyncSession) -> Cart:
        """
        Увеличение на 1 кол-ва товара в корзине
        :param record: обновляемая запись
        :param session: объект асинхронной сессии
        :return: обновленная запись
        """

        query = update(Cart).where(Cart.id == record.id).values(count=record.count + 1).returning(Cart)

        updated_record = await session.execute(query)
        await session.commit()

        return updated_record.scalar_one_or_none()

    @classmethod
    async def decrement(cls, record: Cart, session: AsyncSession) -> Cart:
        """
        Уменьшение на 1 кол-ва товара в корзине
        :param record: обновляемая запись
        :param session: объект асинхронной сессии
        :return: обновленная запись
        """

        query = update(Cart).where(Cart.id == record.id).values(count=record.count - 1).returning(Cart)

        updated_record = await session.execute(query)
        await session.commit()

        return updated_record.scalar_one_or_none()

    @classmethod
    async def delete(cls, record: Cart, session: AsyncSession) -> None:
        """
        Удаление записи о товаре в корзине
        :param record: запись для удаления
        :param session: объект асинхронной сессии
        :return: None
        """
        query = delete(Cart).where(Cart.id == record.id)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def clear(cls, session: AsyncSession) -> None:
        """
        Очистка корзины
        :param session: объект асинхронной сессии
        :return: None
        """

        query = delete(Cart)
        await session.execute(query)
        await session.commit()
