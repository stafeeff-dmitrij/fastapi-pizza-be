from pydantic import BaseModel


class CategorySchema(BaseModel):
    """
    Схема для возврата данных о категории пиццы
    """

    id: int
    name: str
