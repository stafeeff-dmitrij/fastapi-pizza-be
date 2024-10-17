from enum import Enum


class DoughType(Enum):
    """
    Тип теста пиццы
    """
    slim = "Тонкое"
    traditional = "Традиционное"


class SizeType(Enum):
    """
    Размеры пиццы, см.
    """
    small = 26
    average = 30
    big = 40


class SortType(Enum):
    """
    Сортировка
    """
    popular = 'popular'
    price = 'price'
    name = 'name'
