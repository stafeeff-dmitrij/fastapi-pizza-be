from typing import Optional

from fastapi import Depends
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.pizza.repositories.pizza import PizzaRepository
from src.pizza.schemas.pizza import PizzaSchema
from src.router import BaseRouter


router = BaseRouter(tags=['Пиццы'])

# кастомный тип возвращаемых данных (меняем кол-во записей по умолчанию)
# в Page передаем схему PizzaSchema, поэтому в response_model не нужно указывать PizzaSchema!
CustomPage = CustomizedPage[Page[PizzaSchema], UseParamsFields(size=8)]


@router.get(
    '/pizzas',
    name="Возврат пицц",
    description="Возврат всех пицц с возможностью фильтрации по названию и пагинацией",
    response_model=CustomPage,
    responses={
        status.HTTP_200_OK: {'model': CustomPage}
    },
)
async def get_pizzas(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    sort_type: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат пицц
    """

    # возврат query-запроса
    query = await PizzaRepository.get_list(
        name=search,
        category_id=category_id,
        sort_type=sort_type,
    )

    # fastapi_pagination сам дополняет query-запрос с учетом пагинации
    return await paginate(session, query)
