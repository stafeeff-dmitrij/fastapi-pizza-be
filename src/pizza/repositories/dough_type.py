from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pizza.models import PizzaDoughType


class DoughTypeRepository:
    """
    Возврат типов теста для пицц
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> list[PizzaDoughType]:
        """
        Возврат типов теста для пицц
        :param session: объект асинхронной сессии
        :return: список с типами теста
        """

        query = select(PizzaDoughType)
        dough_types = await session.execute(query)

        return dough_types.scalars().all()

    @classmethod
    async def get(cls, dough_type_id: int, session: AsyncSession) -> PizzaDoughType | None:
        """
        Возврат записи о типе теста пиццы
        :param dough_type_id: идентификатор записи
        :param session: объект асинхронной сессии
        :return: запись о типе теста
        """
        query = select(PizzaDoughType).where(PizzaDoughType.id == dough_type_id)
        dough_type = await session.execute(query)

        return dough_type.scalar_one_or_none()
