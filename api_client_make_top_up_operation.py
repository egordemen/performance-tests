"""Скрипт для создания операции пополнения счёта.

Выполняет следующие действия:
1. Создаёт пользователя.
2. Открывает дебетовый счёт.
3. Создаёт операцию пополнения счёта.
4. Выводит ответы сервера в лог.
"""

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client


def main() -> None:
    """Создаёт пользователя, открывает счёт и выполняет пополнение."""
    users_client = build_users_gateway_http_client()
    accounts_client = build_accounts_gateway_http_client()
    operations_client = build_operations_gateway_http_client()

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