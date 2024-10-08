from pydantic import BaseModel


class SizeSchema(BaseModel):
    """
    Схема для возврата данных о размерах пицц
    """

    id: str
    value: int
    price_rise: int
