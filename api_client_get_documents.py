"""Скрипт для получения документов по счёту через http-gateway.

Скрипт выполняет следующие действия:
1. Создаёт пользователя с помощью :class:`UsersGatewayHTTPClient`.
2. Открывает кредитный счёт с помощью :class:`AccountsGatewayHTTPClient`.
3. Получает документ тарифа с помощью :class:`DocumentsGatewayHTTPClient`.
4. Получает документ контракта с помощью :class:`DocumentsGatewayHTTPClient`.

В лог выводятся ответы сервера по каждой созданной сущности.
"""

from __future__ import annotations

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client


def main() -> None:
    """Выполняет сценарий получения документов по счёту."""
    # Инициализация API-клиентов.
    users_client = build_users_gateway_http_client()
    accounts_client = build_accounts_gateway_http_client()
    documents_client = build_documents_gateway_http_client()

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