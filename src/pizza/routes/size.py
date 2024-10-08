from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.pizza.repositories.size import SizeRepository
from src.pizza.schemas.size import SizeSchema
from src.router import BaseRouter


router = BaseRouter(tags=['Размеры пицц'])

@router.get(
    '/sizes',
    name="Возврат размеров пицц",
    description="Возврат всех возможных размеров пицц",
    response_model=list[SizeSchema],
    responses={
        status.HTTP_200_OK: {'model': list[SizeSchema]}
    },
)
async def get_sizes(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возврат размеров пицц
    """
    sizes = await SizeRepository.get_list(session=session)

    return sizes
