from pydantic import BaseModel, Field


class PizzaSchema(BaseModel):
    """
    Схема для возврата данных о пицце
    """

    # вывод id под полем pizza_id
    id: int = Field(serialization_alias='pizza_id')
    name: str
    image: str
    price: float
    category_id: int


class PizzaDetailsSchema(PizzaSchema):
    """
    Схема для возврата всех данных о пицце
    """

    description: str
