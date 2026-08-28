"""HTTP-клиент для работы с документами через http-gateway.

Модуль содержит класс :class:`DocumentsGatewayHTTPClient`, который предоставляет
методы для получения документов (тарифа и контракта) по счёту через эндпоинты
``/api/v1/documents`` сервиса http-gateway.
"""

from __future__ import annotations
from typing import TypedDict
import httpx
from clients.http.client import HTTPClient

TARIFF_DOCUMENT_ENDPOINT = "/api/v1/documents/tariff-document"
CONTRACT_DOCUMENT_ENDPOINT = "/api/v1/documents/contract-document"


class DocumentDict(TypedDict):
    """Структура документа, возвращаемого сервисом.

    Атрибуты:
        url: URL-адрес документа.
        document: Текстовое содержимое документа.
    """

    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """Структура ответа на запрос документа тарифа.

    Атрибуты:
        tariff: Документ тарифа.
    """

    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """Структура ответа на запрос документа контракта.

    Атрибуты:
        contract: Документ контракта.
    """

    contract: DocumentDict


class DocumentsGatewayHTTPClient(HTTPClient):
    """HTTP-клиент для работы с документами через http-gateway.

    Предоставляет методы для получения документов тарифа и контракта по счёту,
    обращаясь к эндпоинтам ``/api/v1/documents`` сервиса http-gateway.

    Наследует базовую логику работы с HTTP-запросами от :class:`HTTPClient`.
    """

    def get_tariff_document_api(self, account_id: str) -> httpx.Response:
        """Выполняет GET-запрос на получение документа тарифа.

        Отправляет запрос к эндпоинту
        ``/api/v1/documents/tariff-document/{account_id}`` для получения
        документа тарифа по идентификатору счёта.

        Аргументы:
            account_id: Идентификатор счёта, для которого запрашивается тариф.

        Возвращает:
            httpx.Response: Ответ сервера с документом тарифа.
        """
        with self._client() as client:
            return client.get(self._url(f"{TARIFF_DOCUMENT_ENDPOINT}/{account_id}"))

    def get_contract_document_api(self, account_id: str) -> httpx.Response:
        """Выполняет GET-запрос на получение документа контракта.

        Отправляет запрос к эндпоинту
        ``/api/v1/documents/contract-document/{account_id}`` для получения
        документа контракта по идентификатору счёта.

        Аргументы:
            account_id: Идентификатор счёта, для которого запрашивается контракт.

        Возвращает:
            httpx.Response: Ответ сервера с документом контракта.
        """
        with self._client() as client:
            return client.get(self._url(f"{CONTRACT_DOCUMENT_ENDPOINT}/{account_id}"))

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """Получает документ тарифа по счёту.

        Выполняет запрос к API через :meth:`get_tariff_document_api`, извлекает
        JSON-ответ и возвращает его.

        Аргументы:
            account_id: Идентификатор счёта, для которого запрашивается тариф.

        Возвращает:
            GetTariffDocumentResponseDict: JSON-ответ сервера с документом тарифа.
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """Получает документ контракта по счёту.

        Выполняет запрос к API через :meth:`get_contract_document_api`, извлекает
        JSON-ответ и возвращает его.

        Аргументы:
            account_id: Идентификатор счёта, для которого запрашивается контракт.

        Возвращает:
            GetContractDocumentResponseDict: JSON-ответ сервера с документом
                контракта.
        """
        response = self.get_contract_document_api(account_id)
        return response.json()

    def close(self) -> None:
        """Закрывает HTTP-клиент и освобождает ресурсы.

        Так как каждый запрос использует собственный контекстный менеджер
        :class:`httpx.Client`, дополнительных действий не требуется.
        """
        return None


def build_documents_gateway_http_client(
    base_url: str = "http://localhost:8003",
) -> DocumentsGatewayHTTPClient:
    """Создаёт и возвращает экземпляр :class:`DocumentsGatewayHTTPClient`.

    Аргументы:
        base_url: Базовый URL сервиса http-gateway.

    Возвращает:
        DocumentsGatewayHTTPClient: Настроенный клиент для работы с документами.
    """
    return DocumentsGatewayHTTPClient(base_url=base_url)