from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base
from src.pizza.models import Pizza, PizzaDoughType, PizzaSize


class Cart(Base):
    """
    Корзина
    """

    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    pizza_id: Mapped[int] = mapped_column(ForeignKey('pizza.id', ondelete='RESTRICT'))
    type_id: Mapped[int] = mapped_column(ForeignKey('dough_type.id', ondelete='RESTRICT'))
    size_id: Mapped[int] = mapped_column(ForeignKey('pizza_size.id', ondelete='RESTRICT'))
    count: Mapped[int] = mapped_column(default=1)

    pizza: Mapped[Pizza] = relationship("Pizza", lazy='joined')
    type: Mapped[PizzaDoughType] = relationship("PizzaDoughType", lazy='joined')
    size: Mapped[PizzaSize] = relationship("PizzaSize", lazy='joined')

    @hybrid_property
    def price(self) -> float:
        """
        Стоимость позиции с учетом типа теста, размера и кол-ва пицц
        """
        position_cost = round((self.pizza.price + (self.pizza.price * self.type.price_rise / 100 ) +
                               (self.pizza.price * self.size.price_rise / 100)) * self.count, 2)
        return position_cost

