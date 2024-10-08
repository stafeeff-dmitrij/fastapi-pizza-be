from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pizza.models import PizzaSize


class SizeRepository:
    """
    Возврат размеров пицц
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> list[PizzaSize]:
        """
        Возврат размеров пицц
        :param session: объект асинхронной сессии
        :return: список с размерами
        """

        query = select(PizzaSize)
        sizes = await session.execute(query)

        return sizes.scalars().all()

    @classmethod
    async def get(cls, size_id: int, session: AsyncSession) -> PizzaSize | None:
        """
        Возврат записи о размере пиццы
        :param size_id: идентификатор записи
        :param session: объект асинхронной сессии
        :return: объект записи о размере пиццы
        """
        query = select(PizzaSize).where(PizzaSize.id == size_id)
        size = await session.execute(query)

        return size.scalar_one_or_none()
