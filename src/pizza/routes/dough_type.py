from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.pizza.repositories.dough_type import DoughTypeRepository
from src.pizza.schemas.dough_type import DoughTypeSchema
from src.router import BaseRouter


router = BaseRouter(tags=['Типы теста для пицц'])

@router.get(
    '/dough_types',
    name="Возврат типов теста для пицц",
    description="Возврат всех возможных типов теста для пицц",
    response_model=list[DoughTypeSchema],
    responses={
        status.HTTP_200_OK: {'model': list[DoughTypeSchema]}
    },
)
async def get_dough_types(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат типов теста для пицц
    """
    dough_types = await DoughTypeRepository.get_list(session=session)

    return dough_types
