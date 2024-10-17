from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.pizza.constants import SortType
from src.pizza.models import Pizza


class PizzaRepository:
    """
    Возврат пицц
    """

    @classmethod
    async def get_list(
            cls,
            name: str = None,
            category_id: int = None,
            sort_type: str = None,
    ) -> select:
        """
        Фильтрация и возврат пицц
        :param name: название пиццы
        :param category_id: id категории
        :param sort_type: тип сортировки
        :param session: объект асинхронной сессии
        :return: список с товарами
        """
        query = select(Pizza)

        if category_id:
            query = query.where(Pizza.category_id == category_id)

        if sort_type:
            if sort_type == SortType.popular.value:
                query = query.order_by(Pizza.id)
            elif sort_type == SortType.price.value:
                query = query.order_by(Pizza.price)
            elif sort_type == SortType.name.value:
                query = query.order_by(Pizza.name)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Некорректное поле для сортировки: {sort_type}'
                )

        if name:
            query = query.where(Pizza.name.ilike(f'%{name}%'))

        return query

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
