"""HTTP-клиент для работы с пользователями через http-gateway.

Модуль содержит класс :class:`UsersGatewayHTTPClient`, который предоставляет
методы для создания пользователей через эндпоинты ``/api/v1/users``
сервиса http-gateway.
"""

from __future__ import annotations
import time
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient


class CreateUserRequestDict(TypedDict):
    """Структура запроса на создание пользователя.

    Атрибуты:
        email: Электронная почта пользователя.
        lastName: Фамилия пользователя.
        firstName: Имя пользователя.
        middleName: Отчество пользователя.
        phoneNumber: Номер телефона пользователя.
    """

    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


class CreateUserResponseDict(TypedDict):
    """Структура ответа на создание пользователя.

    Атрибуты:
        user: Объект созданного пользователя.
    """

    user: dict


class UsersGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы с пользователями через http-gateway.

    Предоставляет методы для создания пользователей, обращаясь к эндпоинтам
    ``/api/v1/users`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Инициализирует клиент для работы с пользователями.

        Аргументы:
            client: Готовый экземпляр :class:`httpx.Client`,
                настроенный вызывающим кодом.
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
        """
        super().__init__(client, base_url)

    def create_user(self) -> CreateUserResponseDict:
        """Создаёт пользователя и возвращает данные о нём.

        Выполняет POST-запрос к эндпоинту ``/api/v1/users`` для создания
        пользователя с уникальной электронной почтой.

        Возвращает:
            CreateUserResponseDict: JSON-ответ сервера с данными созданного
                пользователя.
        """
        unique_email = f"user.{int(time.time())}.{int(time.time() * 1000) % 1000000}@example.com"

        request: CreateUserRequestDict = {
            "email": unique_email,
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "phoneNumber": "string",
        }

        response = self.client.post(
            f"{self.base_url}/api/v1/users", json=request
        )
        response.raise_for_status()
        return response.json()
