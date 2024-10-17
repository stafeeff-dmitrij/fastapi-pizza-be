from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from src.config import ALLOWED_ORIGINS, DEBUG
from src.urls import register_routers


app = FastAPI(title='pizzas', debug=DEBUG)
add_pagination(app)  # подключаем пагинацию

# Регистрация роутеров
register_routers(app)

# URL, с которых разрешено делать запросы на сервер
origins = ALLOWED_ORIGINS.split(',')

# Добавляем в middleware Cors для связки фронта и бэка
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
