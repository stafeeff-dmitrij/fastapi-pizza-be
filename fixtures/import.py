import asyncio
import json
import os

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.pizza.models import Category, Pizza, PizzaDoughType, PizzaSize


class ImportData:

    FOLDERS = ['fixtures', 'data']

    @classmethod
    async def _get_file_path(cls, file: str) -> str:
        """
        Возврат пути до файла с фикстурами
        """
        folders = [folder for folder in cls.FOLDERS]
        folders.append(file)
        file = os.path.join(*folders)

        return file

    @classmethod
    async def get_data(cls, file: str) -> list[dict]:
        """
        Возврат данных из JSON-файла
        """
        file = await cls._get_file_path(file)

        with open(file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    @classmethod
    async def _import_categories(cls, session: AsyncSession) -> None:
        """
        Загрузка данных по категориям
        """

        data = await cls.get_data('categories.json')

        for item in data:
            category = Category(id=item['id'], name=item['name'])
            session.add(category)

        await session.commit()

    @classmethod
    async def _import_pizzas(cls, session: AsyncSession) -> None:
        """
        Загрузка данных по пиццам
        """

        data = await cls.get_data('pizzas.json')

        for item in data:
            pizza = Pizza(
                id=item['id'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                price=item['price'],
                category_id=item['category_id']
            )
            session.add(pizza)

        await session.commit()

    @classmethod
    async def _import_dough_type(cls, session: AsyncSession) -> None:
        """
        Загрузка данных по типам теста для пицц
        """

        data = await cls.get_data('dough_types.json')

        for item in data:
            dough_type = PizzaDoughType(
                id=item['id'],
                name=item['name'],
                price_rise=item['price_rise']
            )
            session.add(dough_type)

        await session.commit()

    @classmethod
    async def _import_sizes(cls, session: AsyncSession) -> None:
        """
        Загрузка данных по размерам пицц
        """

        data = await cls.get_data('sizes.json')

        for item in data:
            size = PizzaSize(
                id=item['id'],
                value=item['value'],
                price_rise=item['price_rise']
            )
            session.add(size)

        await session.commit()


    @classmethod
    async def import_data(cls):

        async with async_session_maker() as session:
            await cls._import_categories(session=session)
            await cls._import_pizzas(session=session)
            await cls._import_dough_type(session=session)
            await cls._import_sizes(session=session)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ImportData.import_data())
