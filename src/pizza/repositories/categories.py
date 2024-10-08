from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pizza.models import Category


class CategoryRepository:
    """
    Возврат категорий пицц
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> list[Category]:
        """
        Возврат категорий пицц
        :param session: объект асинхронной сессии
        :return: список с категориями
        """
        query = select(Category)
        pizzas = await session.execute(query)

        return pizzas.scalars().all()

    @classmethod
    async def get(cls, category_id: int, session: AsyncSession) -> Category | None:
        """
        Возврат записи о категории
        :param category_id: идентификатор категории
        :param session: объект асинхронной сессии
        :return: объект записи о категории
        """
        query = select(Category).where(Category.id == category_id)
        category = await session.execute(query)

        return category.scalar_one_or_none()
