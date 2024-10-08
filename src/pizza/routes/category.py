from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.pizza.repositories.categories import CategoryRepository
from src.pizza.schemas.category import CategorySchema
from src.router import BaseRouter


router = BaseRouter(tags=['Категории'])

@router.get(
    '/categories',
    name="Возврат категорий",
    description="Возврат всех категорий п пиццам",
    response_model=list[CategorySchema],
    responses={
        status.HTTP_200_OK: {'model': list[CategorySchema]}
    },
)
async def get_categories(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат категорий
    """

    categories = await CategoryRepository.get_list(session=session)

    return categories
