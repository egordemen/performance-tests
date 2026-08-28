"""HTTP-клиент для работы с пользователями через http-gateway.

Модуль содержит класс :class:`UsersGatewayHTTPClient`, который предоставляет
методы для создания пользователей через эндпоинты ``/api/v1/users``
сервиса http-gateway.
"""

from __future__ import annotations
import time
from typing import TypedDict
from clients.http.client import HTTPClient

USERS_ENDPOINT = "/api/v1/users"


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

        with self._client() as client:
            response = client.post(self._url(USERS_ENDPOINT), json=request)
            response.raise_for_status()
            return response.json()

    def close(self) -> None:
        """Закрывает HTTP-клиент и освобождает ресурсы.

        Так как каждый запрос использует собственный контекстный менеджер
        :class:`httpx.Client`, дополнительных действий не требуется.
        """
        return None


def build_users_gateway_http_client(base_url: str = "http://localhost:8003") -> UsersGatewayHTTPClient:
    """Создаёт и возвращает экземпляр :class:`UsersGatewayHTTPClient`.

    Аргументы:
        base_url: Базовый URL сервиса http-gateway.

    Возвращает:
        UsersGatewayHTTPClient: Настроенный клиент для работы с пользователями.
    """
    return UsersGatewayHTTPClient(base_url=base_url)