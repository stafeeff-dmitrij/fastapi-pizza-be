from pydantic import BaseModel


class PizzaSchema(BaseModel):
    """
    Схема для возврата данных о пицце
    """

    id: int
    name: str
    image: str
    price: float
    category_id: int
