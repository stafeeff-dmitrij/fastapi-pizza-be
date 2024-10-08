from sqlalchemy import String, Numeric, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Category(Base):
    """
    Категория
    """

    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100))


class Pizza(Base):
    """
    Пицца
    """

    __tablename__ = 'pizza'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    image: Mapped[str] = mapped_column(String(250))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='RESTRICT'))

    category: Mapped[Category] = relationship("Category", lazy='joined')


class PizzaDoughType(Base):
    """
    Типы теста
    """

    __tablename__ = 'dough_type'

    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    price_rise: Mapped[int] = mapped_column(CheckConstraint('price_rise >= 0 AND price_rise <= 100'))


class PizzaSize(Base):
    """
    Размеры пицц
    """

    __tablename__ = 'pizza_size'

    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    value: Mapped[int] = mapped_column()
    price_rise: Mapped[int] = mapped_column(CheckConstraint('price_rise >= 0 AND price_rise <= 100'))
