"""HTTP-клиент для работы со счетами через http-gateway.

Модуль содержит класс :class:`AccountsGatewayHTTPClient`, который предоставляет
методы для открытия счетов через эндпоинты ``/api/v1/accounts``
сервиса http-gateway.
"""

from __future__ import annotations
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient


class OpenCreditCardAccountRequestDict(TypedDict):
    """Структура запроса на открытие кредитного счёта.

    Атрибуты:
        userId: Идентификатор пользователя, для которого открывается счёт.
    """

    userId: str


class OpenCreditCardAccountResponseDict(TypedDict):
    """Структура ответа на открытие кредитного счёта.

    Атрибуты:
        account: Объект открытого счёта.
    """

    account: dict


class OpenDebitCardAccountRequestDict(TypedDict):
    """Структура запроса на открытие дебетового счёта.

    Атрибуты:
        userId: Идентификатор пользователя, для которого открывается счёт.
    """

    userId: str


class OpenDebitCardAccountResponseDict(TypedDict):
    """Структура ответа на открытие дебетового счёта.

    Атрибуты:
        account: Объект открытого счёта.
    """

    account: dict


class AccountsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы со счетами через http-gateway.

    Предоставляет методы для открытия счетов, обращаясь к эндпоинтам
    ``/api/v1/accounts`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Инициализирует клиент для работы со счетами.

        Аргументы:
            client: Готовый экземпляр :class:`httpx.Client`,
                настроенный вызывающим кодом.
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
        """
        super().__init__(client, base_url)

    def open_credit_card_account(
        self, user_id: str
    ) -> OpenCreditCardAccountResponseDict:
        """Открывает кредитный счёт для пользователя.

        Выполняет POST-запрос к эндпоинту
        ``/api/v1/accounts/open-credit-card-account`` для открытия кредитного
        счёта с привязанными картами.

        Аргументы:
            user_id: Идентификатор пользователя, для которого открывается счёт.

        Возвращает:
            OpenCreditCardAccountResponseDict: JSON-ответ сервера с данными
                открытого счёта.
        """
        request: OpenCreditCardAccountRequestDict = {"userId": user_id}

        response = self.client.post(
            f"{self.base_url}/api/v1/accounts/open-credit-card-account", json=request
        )
        response.raise_for_status()
        return response.json()

    def open_debit_card_account(
        self, user_id: str
    ) -> OpenDebitCardAccountResponseDict:
        """Открывает дебетовый счёт для пользователя.

        Выполняет POST-запрос к эндпоинту
        ``/api/v1/accounts/open-debit-card-account`` для открытия дебетового
        счёта с привязанными картами.

        Аргументы:
            user_id: Идентификатор пользователя, для которого открывается счёт.

        Возвращает:
            OpenDebitCardAccountResponseDict: JSON-ответ сервера с данными
                открытого счёта.
        """
        request: OpenDebitCardAccountRequestDict = {"userId": user_id}

        response = self.client.post(
            f"{self.base_url}/api/v1/accounts/open-debit-card-account", json=request
        )
        response.raise_for_status()
        return response.json()
