from pydantic import BaseModel


class DoughTypeSchema(BaseModel):
    """
    Схема для возврата данных о типе теста пиццы
    """

    id: str
    name: str
    price_rise: int
