"""Скрипт для получения документов по счёту через http-gateway.

Скрипт выполняет следующие действия:
1. Создаёт пользователя с помощью :class:`UsersGatewayHTTPClient`.
2. Открывает кредитный счёт с помощью :class:`AccountsGatewayHTTPClient`.
3. Получает документ тарифа с помощью :class:`DocumentsGatewayHTTPClient`.
4. Получает документ контракта с помощью :class:`DocumentsGatewayHTTPClient`.

В лог выводятся ответы сервера по каждой созданной сущности.
"""

from __future__ import annotations

import httpx

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.documents.client import DocumentsGatewayHTTPClient
from clients.http.gateway.users.client import UsersGatewayHTTPClient

BASE_URL = "http://localhost:8003"


def main() -> None:
    """Выполняет сценарий получения документов по счёту."""
    with httpx.Client(timeout=30.0) as client:
        # Инициализация API-клиентов с общим httpx.Client.
        users_client = UsersGatewayHTTPClient(client, BASE_URL)
        accounts_client = AccountsGatewayHTTPClient(client, BASE_URL)
        documents_client = DocumentsGatewayHTTPClient(client, BASE_URL)

        # 1. Создание пользователя.
        create_user_response = users_client.create_user()
        print(f"Create user response: {create_user_response}")

        user_id = create_user_response["user"]["id"]

        # 2. Открытие кредитного счёта.
        open_account_response = accounts_client.open_credit_card_account(user_id)
        print(f"Open credit card account response: {open_account_response}")

        account_id = open_account_response["account"]["id"]

        # 3. Получение документа тарифа.
        tariff_document = documents_client.get_tariff_document(account_id)
        print(f"Get tariff document response: {tariff_document}")

        # 4. Получение документа контракта.
        contract_document = documents_client.get_contract_document(account_id)
        print(f"Get contract document response: {contract_document}")


if __name__ == "__main__":
    main()
