"""HTTP-клиент для работы с операциями через http-gateway.

Модуль содержит класс :class:`OperationsGatewayHTTPClient`, который
предоставляет методы для получения информации об операциях, получения
чеков, списков и статистики, а также для создания различных типов
операций через эндпоинты ``/api/v1/operations`` сервиса http-gateway.
"""

from __future__ import annotations
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient

OPERATIONS_ENDPOINT = "/api/v1/operations"
OPERATION_RECEIPT_ENDPOINT = "/api/v1/operations/operation-receipt"
OPERATIONS_SUMMARY_ENDPOINT = "/api/v1/operations/operations-summary"
MAKE_FEE_OPERATION_ENDPOINT = "/api/v1/operations/make-fee-operation"
MAKE_TOP_UP_OPERATION_ENDPOINT = "/api/v1/operations/make-top-up-operation"
MAKE_CASHBACK_OPERATION_ENDPOINT = "/api/v1/operations/make-cashback-operation"
MAKE_TRANSFER_OPERATION_ENDPOINT = "/api/v1/operations/make-transfer-operation"
MAKE_PURCHASE_OPERATION_ENDPOINT = "/api/v1/operations/make-purchase-operation"
MAKE_BILL_PAYMENT_OPERATION_ENDPOINT = "/api/v1/operations/make-bill-payment-operation"
MAKE_CASH_WITHDRAWAL_OPERATION_ENDPOINT = "/api/v1/operations/make-cash-withdrawal-operation"


class GetOperationsQueryDict(TypedDict):
    """Структура query-параметров для получения списка операций.

    Атрибуты:
        accountId: Идентификатор счёта, по которому запрашиваются операции.
    """

    accountId: str


class GetOperationsSummaryQueryDict(TypedDict):
    """Структура query-параметров для получения статистики по операциям.

    Атрибуты:
        accountId: Идентификатор счёта, по которому запрашивается статистика.
    """

    accountId: str


class MakeOperationRequestDict(TypedDict):
    """Базовая структура запроса на создание операции.

    Содержит общие поля, характерные для всех типов операций.

    Атрибуты:
        status: Статус операции (например, ``IN_PROGRESS``).
        amount: Сумма операции.
        cardId: Идентификатор карты, по которой выполняется операция.
        accountId: Идентификатор счёта, по которому выполняется операция.
    """

    status: str
    amount: float
    cardId: str
    accountId: str


class MakeFeeOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции комиссии.

    Наследует общие поля из :class:`MakeOperationRequestDict`.
    """

    pass


class MakeTopUpOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции пополнения.

    Наследует общие поля из :class:`MakeOperationRequestDict`.
    """

    pass


class MakeCashbackOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции кэшбэка.

    Наследует общие поля из :class:`MakeOperationRequestDict`.
    """

    pass


class MakeTransferOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции перевода.

    Наследует общие поля из :class:`MakeOperationRequestDict` и добавляет
    информацию о получателе перевода.

    Атрибуты:
        recipientAccountId: Идентификатор счёта получателя перевода.
    """

    recipientAccountId: str


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции покупки.

    Наследует общие поля из :class:`MakeOperationRequestDict` и добавляет
    категорию покупки.

    Атрибуты:
        category: Категория покупки (например, ``taxi``).
    """

    category: str


class MakeBillPaymentOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции оплаты по счёту.

    Наследует общие поля из :class:`MakeOperationRequestDict`.
    """

    pass


class MakeCashWithdrawalOperationRequestDict(MakeOperationRequestDict):
    """Структура запроса на создание операции снятия наличных.

    Наследует общие поля из :class:`MakeOperationRequestDict`.
    """

    pass


class OperationsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы с операциями через http-gateway.

    Предоставляет методы для получения информации об операциях, чеках,
    списках и статистике, а также для создания различных типов операций,
    обращаясь к эндпоинтам ``/api/v1/operations`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def get_operation_api(self, operation_id: str) -> httpx.Response:
        """Выполняет GET-запрос на получение информации об операции.

        Отправляет запрос к эндпоинту ``/api/v1/operations/{operation_id}``
        для получения информации об операции по её идентификатору.

        Аргументы:
            operation_id: Идентификатор операции.

        Возвращает:
            httpx.Response: Ответ сервера с информацией об операции.
        """
        with self._client() as client:
            return client.get(self._url(f"{OPERATIONS_ENDPOINT}/{operation_id}"))

    def get_operation_receipt_api(self, operation_id: str) -> httpx.Response:
        """Выполняет GET-запрос на получение чека по операции.

        Отправляет запрос к эндпоинту
        ``/api/v1/operations/operation-receipt/{operation_id}`` для получения
        чека по операции по её идентификатору.

        Аргументы:
            operation_id: Идентификатор операции.

        Возвращает:
            httpx.Response: Ответ сервера с чеком по операции.
        """
        with self._client() as client:
            return client.get(self._url(f"{OPERATION_RECEIPT_ENDPOINT}/{operation_id}"))

    def get_operations_api(self, query: GetOperationsQueryDict) -> httpx.Response:
        """Выполняет GET-запрос на получение списка операций счёта.

        Отправляет запрос к эндпоинту ``/api/v1/operations`` для получения
        списка операций для определённого счёта.

        Аргументы:
            query: Query-параметры запроса, содержащие ``accountId``.

        Возвращает:
            httpx.Response: Ответ сервера со списком операций.
        """
        with self._client() as client:
            return client.get(self._url(OPERATIONS_ENDPOINT), params=query)

    def get_operations_summary_api(
        self, query: GetOperationsSummaryQueryDict
    ) -> httpx.Response:
        """Выполняет GET-запрос на получение статистики по операциям.

        Отправляет запрос к эндпоинту ``/api/v1/operations/operations-summary``
        для получения статистики по операциям для определённого счёта.

        Аргументы:
            query: Query-параметры запроса, содержащие ``accountId``.

        Возвращает:
            httpx.Response: Ответ сервера со статистикой по операциям.
        """
        with self._client() as client:
            return client.get(self._url(OPERATIONS_SUMMARY_ENDPOINT), params=query)

    def make_fee_operation_api(
        self, request: MakeFeeOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции комиссии.

        Отправляет запрос к эндпоинту ``/api/v1/operations/make-fee-operation``
        для создания операции комиссии.

        Аргументы:
            request: Структура запроса с данными операции комиссии.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_FEE_OPERATION_ENDPOINT), json=request)

    def make_top_up_operation_api(
        self, request: MakeTopUpOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции пополнения.

        Отправляет запрос к эндпоинту ``/api/v1/operations/make-top-up-operation``
        для создания операции пополнения.

        Аргументы:
            request: Структура запроса с данными операции пополнения.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_TOP_UP_OPERATION_ENDPOINT), json=request)

    def make_cashback_operation_api(
        self, request: MakeCashbackOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции кэшбэка.

        Отправляет запрос к эндпоинту ``/api/v1/operations/make-cashback-operation``
        для создания операции кэшбэка.

        Аргументы:
            request: Структура запроса с данными операции кэшбэка.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_CASHBACK_OPERATION_ENDPOINT), json=request)

    def make_transfer_operation_api(
        self, request: MakeTransferOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции перевода.

        Отправляет запрос к эндпоинту ``/api/v1/operations/make-transfer-operation``
        для создания операции перевода.

        Аргументы:
            request: Структура запроса с данными операции перевода.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_TRANSFER_OPERATION_ENDPOINT), json=request)

    def make_purchase_operation_api(
        self, request: MakePurchaseOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции покупки.

        Отправляет запрос к эндпоинту ``/api/v1/operations/make-purchase-operation``
        для создания операции покупки.

        Аргументы:
            request: Структура запроса с данными операции покупки.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_PURCHASE_OPERATION_ENDPOINT), json=request)

    def make_bill_payment_operation_api(
        self, request: MakeBillPaymentOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции оплаты по счёту.

        Отправляет запрос к эндпоинту
        ``/api/v1/operations/make-bill-payment-operation`` для создания операции
        оплаты по счёту.

        Аргументы:
            request: Структура запроса с данными операции оплаты по счёту.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(self._url(MAKE_BILL_PAYMENT_OPERATION_ENDPOINT), json=request)

    def make_cash_withdrawal_operation_api(
        self, request: MakeCashWithdrawalOperationRequestDict
    ) -> httpx.Response:
        """Выполняет POST-запрос на создание операции снятия наличных.

        Отправляет запрос к эндпоинту
        ``/api/v1/operations/make-cash-withdrawal-operation`` для создания
        операции снятия наличных денег.

        Аргументы:
            request: Структура запроса с данными операции снятия наличных.

        Возвращает:
            httpx.Response: Ответ сервера на запрос создания операции.
        """
        with self._client() as client:
            return client.post(
                self._url(MAKE_CASH_WITHDRAWAL_OPERATION_ENDPOINT), json=request
            )

    def close(self) -> None:
        """Закрывает HTTP-клиент и освобождает ресурсы.

        Так как каждый запрос использует собственный контекстный менеджер
        :class:`httpx.Client`, дополнительных действий не требуется.
        """
        return None