from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pizza.models import Pizza


class PizzaRepository:
    """
    Возврат пицц
    """

    @classmethod
    async def get_list(
            cls,
            session: AsyncSession,
            name: str = None,
            category_id: int = None,
            limit: int = None,
            offset: int = None,
    ) -> list[Pizza]:
        """
        Фильтрация и возврат пицц
        :param name: название пиццы
        :param category_id: id категории
        :param limit: кол-во возвращаемых записей
        :param offset: сдвиг в наборе результатов
        :param ids_list: список с идентификаторами для фильтрации товаров
        :param session: объект асинхронной сессии
        :return: список с товарами
        """
        query = select(Pizza)

        if category_id:
            query = query.where(Pizza.category_id == category_id)

        if name:
            query = query.where(Pizza.name.ilike(f'%{name}%'))

        if limit is not None and offset is not None:
            query = query.limit(limit).offset(offset)

        pizzas = await session.execute(query)

        return pizzas.scalars().all()

    @classmethod
    async def get(cls, pizza_id: int, session: AsyncSession) -> Pizza | None:
        """
        Возврат пиццы по id
        :param pizza_id: идентификатор пиццы
        :param session: объект асинхронной сессии
        :return: объект пиццы | None
        """
        query = select(Pizza).where(Pizza.id == pizza_id)
        pizza = await session.execute(query)

        return pizza.scalar_one_or_none()
