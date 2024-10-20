from pydantic import BaseModel, Field, computed_field

from src.pizza.schemas.pizza import PizzaSchema


class CartSchema(BaseModel):
    """
    Схема для возврата данных о позиции в корзине
    """

    id: int
    pizza_id: int
    size_id: str
    type_id: str
    price: float
    count: int

    @computed_field()
    def name(self) -> str:
        return self.pizza.name

    @computed_field()
    def image(self) -> str:
        return self.pizza.image

    pizza: PizzaSchema = Field(exclude=True)


class PizzaAddToCartSchema(BaseModel):
    """
    Схема для добавления пиццы в корзину
    """

    pizza_id: int
    type_id: str
    size_id: str
