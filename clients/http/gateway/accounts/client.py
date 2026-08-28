"""HTTP-клиент для работы со счетами через http-gateway.

Модуль содержит класс :class:`AccountsGatewayHTTPClient`, который предоставляет
методы для открытия счетов через эндпоинты ``/api/v1/accounts``
сервиса http-gateway.
"""

from __future__ import annotations
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient

OPEN_CREDIT_CARD_ACCOUNT_ENDPOINT = "/api/v1/accounts/open-credit-card-account"


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


class AccountsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы со счетами через http-gateway.

    Предоставляет методы для открытия счетов, обращаясь к эндпоинтам
    ``/api/v1/accounts`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

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

        with self._client() as client:
            response = client.post(self._url(OPEN_CREDIT_CARD_ACCOUNT_ENDPOINT), json=request)
            response.raise_for_status()
            return response.json()

    def close(self) -> None:
        """Закрывает HTTP-клиент и освобождает ресурсы.

        Так как каждый запрос использует собственный контекстный менеджер
        :class:`httpx.Client`, дополнительных действий не требуется.
        """
        return None


def build_accounts_gateway_http_client(
    base_url: str = "http://localhost:8003",
) -> AccountsGatewayHTTPClient:
    """Создаёт и возвращает экземпляр :class:`AccountsGatewayHTTPClient`.

    Аргументы:
        base_url: Базовый URL сервиса http-gateway.

    Возвращает:
        AccountsGatewayHTTPClient: Настроенный клиент для работы со счетами.
    """
    return AccountsGatewayHTTPClient(base_url=base_url)