"""Скрипт для создания операции пополнения счёта.

Выполняет следующие действия:
1. Создаёт пользователя.
2. Открывает дебетовый счёт.
3. Создаёт операцию пополнения счёта.
4. Выводит ответы сервера в лог.
"""

from __future__ import annotations

import httpx

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.operations.client import OperationsGatewayHTTPClient
from clients.http.gateway.users.client import UsersGatewayHTTPClient

BASE_URL = "http://localhost:8003"


def main() -> None:
    """Создаёт пользователя, открывает счёт и выполняет пополнение."""
    with httpx.Client(timeout=30.0) as client:
        users_client = UsersGatewayHTTPClient(client, BASE_URL)
        accounts_client = AccountsGatewayHTTPClient(client, BASE_URL)
        operations_client = OperationsGatewayHTTPClient(client, BASE_URL)

        # 1. Создаём пользователя.
        create_user_response = users_client.create_user()
        print(f"Create user response: {create_user_response}")
        user_id = create_user_response["user"]["id"]

        # 2. Открываем дебетовый счёт.
        open_account_response = accounts_client.open_debit_card_account(user_id)
        print(f"Open debit card account response: {open_account_response}")
        account_id = open_account_response["account"]["id"]
        card_id = open_account_response["account"]["cards"][0]["id"]

        # 3. Создаём операцию пополнения.
        make_top_up_response = operations_client.make_top_up_operation(card_id, account_id)
        print(f"Make top up operation response: {make_top_up_response}")


if __name__ == "__main__":
    main()
