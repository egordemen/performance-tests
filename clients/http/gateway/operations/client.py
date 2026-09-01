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
        cardId: Идентификатор карты, по которому выполняется операция.
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


class OperationDict(TypedDict):
    """Структура операции.

    Атрибуты:
        id: Идентификатор операции.
        type: Тип операции (FEE, TOP_UP, PURCHASE, CASHBACK, TRANSFER, BILL_PAYMENT, CASH_WITHDRAWAL).
        status: Статус операции (FAILED, COMPLETED, IN_PROGRESS, UNSPECIFIED).
        amount: Сумма операции.
        cardId: Идентификатор карты.
        category: Категория операции.
        createdAt: Дата создания операции.
        accountId: Идентификатор счёта.
    """

    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """Структура чека по операции.

    Атрибуты:
        url: URL-адрес документа чека.
        document: Текстовое содержимое чека.
    """

    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """Структура статистики по операциям.

    Атрибуты:
        spentAmount: Общая сумма расходов.
        receivedAmount: Общая сумма поступлений.
        cashbackAmount: Общая сумма кэшбэка.
    """

    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationResponseDict(TypedDict):
    """Структура ответа на запрос информации об операции.

    Атрибуты:
        operation: Объект операции.
    """

    operation: dict


class GetOperationsResponseDict(TypedDict):
    """Структура ответа на запрос списка операций.

    Атрибуты:
        operations: Список операций.
    """

    operations: list[OperationDict]


class GetOperationsSummaryResponseDict(TypedDict):
    """Структура ответа на запрос статистики по операциям.

    Атрибуты:
        summary: Статистика по операциям.
    """

    summary: OperationsSummaryDict


class MakeOperationResponseDict(TypedDict):
    """Структура ответа на создание операции.

    Атрибуты:
        operation: Созданная операция.
    """

    operation: dict


class OperationsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы с операциями через http-gateway.

    Предоставляет методы для получения информации об операциях, чеках,
    списках и статистике, а также для создания различных типов операций,
    обращаясь к эндпоинтам ``/api/v1/operations`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Инициализирует клиент для работы с операциями.

        Аргументы:
            client: Готовый экземпляр :class:`httpx.Client`,
                настроенный вызывающим кодом.
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
        """
        super().__init__(client, base_url)

    def get_operation_api(self, operation_id: str) -> httpx.Response:
        """Выполняет GET-запрос на получение информации об операции.

        Отправляет запрос к эндпоинту ``/api/v1/operations/{operation_id}``
        для получения информации об операции по её идентификатору.

        Аргументы:
            operation_id: Идентификатор операции.

        Возвращает:
            httpx.Response: Ответ сервера с информацией об операции.
        """
        return self.client.get(
            f"{self.base_url}/api/v1/operations/{operation_id}"
        )

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
        return self.client.get(
            f"{self.base_url}/api/v1/operations/operation-receipt/{operation_id}"
        )

    def get_operations_api(self, query: GetOperationsQueryDict) -> httpx.Response:
        """Выполняет GET-запрос на получение списка операций счёта.

        Отправляет запрос к эндпоинту ``/api/v1/operations`` для получения
        списка операций для определённого счёта.

        Аргументы:
            query: Query-параметры запроса, содержащие ``accountId``.

        Возвращает:
            httpx.Response: Ответ сервера со списком операций.
        """
        return self.client.get(
            f"{self.base_url}/api/v1/operations", params=query
        )

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
        return self.client.get(
            f"{self.base_url}/api/v1/operations/operations-summary", params=query
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-fee-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-top-up-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-cashback-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-transfer-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-purchase-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-bill-payment-operation", json=request
        )

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
        return self.client.post(
            f"{self.base_url}/api/v1/operations/make-cash-withdrawal-operation", json=request
        )

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """Получает информацию об операции по идентификатору.

        Выполняет запрос к API через :meth:`get_operation_api`, извлекает
        JSON-ответ и возвращает его.

        Аргументы:
            operation_id: Идентификатор операции.

        Возвращает:
            GetOperationResponseDict: JSON-ответ сервера с информацией
                об операции.
        """
        response = self.get_operation_api(operation_id)
        return response.json()

    def get_operation_receipt(
        self, operation_id: str
    ) -> OperationReceiptDict:
        """Получает чек по операции.

        Выполняет запрос к API через :meth:`get_operation_receipt_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            operation_id: Идентификатор операции.

        Возвращает:
            OperationReceiptDict: JSON-ответ сервера с чеком по операции.
        """
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """Получает список операций по счёту.

        Выполняет запрос к API через :meth:`get_operations_api`, извлекает
        JSON-ответ и возвращает его.

        Аргументы:
            account_id: Идентификатор счёта, по которому запрашиваются
                операции.

        Возвращает:
            GetOperationsResponseDict: JSON-ответ сервера со списком
                операций.
        """
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary(
        self, account_id: str
    ) -> GetOperationsSummaryResponseDict:
        """Получает статистику по операциям по счёту.

        Выполняет запрос к API через :meth:`get_operations_summary_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            account_id: Идентификатор счёта, по которому запрашивается
                статистика.

        Возвращает:
            GetOperationsSummaryResponseDict: JSON-ответ сервера со
                статистикой по операциям.
        """
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(query)
        return response.json()

    def make_fee_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию комиссии.

        Формирует запрос и выполняет его через :meth:`make_fee_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией комиссии.
        """
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию пополнения счёта.

        Формирует запрос и выполняет его через :meth:`make_top_up_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией пополнения.
        """
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=1500.11,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию кэшбэка.

        Формирует запрос и выполняет его через :meth:`make_cashback_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией кэшбэка.
        """
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=100.0,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию перевода.

        Формирует запрос и выполняет его через :meth:`make_transfer_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией перевода.
        """
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=500.0,
            cardId=card_id,
            accountId=account_id,
            recipientAccountId=account_id,
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию покупки.

        Формирует запрос и выполняет его через :meth:`make_purchase_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией покупки.
        """
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=250.0,
            cardId=card_id,
            accountId=account_id,
            category="taxi",
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию оплаты по счёту.

        Формирует запрос и выполняет его через :meth:`make_bill_payment_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией оплаты по счёту.
        """
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=1000.0,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation(
        self, card_id: str, account_id: str
    ) -> MakeOperationResponseDict:
        """Создаёт операцию снятия наличных.

        Формирует запрос и выполняет его через :meth:`make_cash_withdrawal_operation_api`,
        извлекает JSON-ответ и возвращает его.

        Аргументы:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Возвращает:
            MakeOperationResponseDict: JSON-ответ сервера с созданной
                операцией снятия наличных.
        """
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=500.0,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()
