"""HTTP-клиент для работы с картами через http-gateway.

Модуль содержит класс :class:`CardsGatewayHTTPClient`, который предоставляет
методы для выпуска виртуальных и физических карт через эндпоинты
``/api/v1/cards`` сервиса http-gateway.
"""

from __future__ import annotations
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient


class IssueVirtualCardRequest(TypedDict):
    """Структура запроса на выпуск виртуальной карты.

    Атрибуты:
        userId: Идентификатор пользователя, для которого выпускается карта.
        accountId: Идентификатор счёта, к которому привязывается карта.
    """

    userId: str
    accountId: str


class IssuePhysicalCardRequest(TypedDict):
    """Структура запроса на выпуск физической карты.

    Атрибуты:
        userId: Идентификатор пользователя, для которого выпускается карта.
        accountId: Идентификатор счёта, к которому привязывается карта.
    """

    userId: str
    accountId: str


class CardsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы с картами через http-gateway.

    Предоставляет методы для выпуска виртуальных и физических карт,
    обращаясь к эндпоинтам ``/api/v1/cards`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Инициализирует клиент для работы с картами.

        Аргументы:
            client: Готовый экземпляр :class:`httpx.Client`,
                настроенный вызывающим кодом.
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
        """
        super().__init__(client, base_url)

    def issue_virtual_card_api(self, request: IssueVirtualCardRequest) -> httpx.Response:
        """Выполняет POST-запрос на выпуск виртуальной карты.

        Отправляет запрос к эндпоинту ``/api/v1/cards/issue-virtual-card``
        для создания виртуальной карты для указанного пользователя и счёта.

        Аргументы:
            request: Структура запроса с данными для выпуска виртуальной карты.
                Содержит поля ``userId`` и ``accountId``.

        Возвращает:
            httpx.Response: Ответ сервера на запрос выпуска виртуальной карты.
        """
        return self.client.post(
            f"{self.base_url}/api/v1/cards/issue-virtual-card",
            json=request,
        )

    def issue_physical_card_api(self, request: IssuePhysicalCardRequest) -> httpx.Response:
        """Выполняет POST-запрос на выпуск физической карты.

        Отправляет запрос к эндпоинту ``/api/v1/cards/issue-physical-card``
        для создания физической карты для указанного пользователя и счёта.

        Аргументы:
            request: Структура запроса с данными для выпуска физической карты.
                Содержит поля ``userId`` и ``accountId``.

        Возвращает:
            httpx.Response: Ответ сервера на запрос выпуска физической карты.
        """
        return self.client.post(
            f"{self.base_url}/api/v1/cards/issue-physical-card",
            json=request,
        )
