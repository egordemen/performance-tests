import time
import httpx


BASE_URL = "http://localhost:8003"

USERS_ENDPOINT = "/api/v1/users"
OPEN_CREDIT_CARD_ACCOUNT_ENDPOINT = "/api/v1/accounts/open-credit-card-account"
MAKE_PURCHASE_OPERATION_ENDPOINT = "/api/v1/operations/make-purchase-operation"
OPERATION_RECEIPT_ENDPOINT = "/api/v1/operations/operation-receipt"


def create_user(client: httpx.Client) -> str:
    unique_email = f"user_{int(time.time())}@example.com"

    payload = {
        "email": unique_email,
        "lastName": "Testov",
        "firstName": "Test",
        "middleName": "Testovich",
        "phoneNumber": "+79990000000",
    }

    response = client.post(f"{BASE_URL}{USERS_ENDPOINT}", json=payload)
    response.raise_for_status()

    user = response.json()["user"]
    user_id = user["id"]
    print(f"Создан пользователь: id={user_id}, email={user.get('email')}")
    return user_id


def open_credit_card_account(client: httpx.Client, user_id: str) -> tuple[str, str]:
    payload = {
        "userId": user_id,
    }

    response = client.post(f"{BASE_URL}{OPEN_CREDIT_CARD_ACCOUNT_ENDPOINT}", json=payload)
    response.raise_for_status()

    data = response.json()
    account_id = data["account"]["id"]
    card_id = data["account"]["cards"][0]["id"]
    print(f"Открыт кредитный счёт: accountId={account_id}, cardId={card_id}")
    return account_id, card_id


def make_purchase_operation(client: httpx.Client, account_id: str, card_id: str) -> str:
    payload = {
        "status": "IN_PROGRESS",
        "amount": 77.99,
        "category": "taxi",
        "cardId": card_id,
        "accountId": account_id,
    }

    response = client.post(f"{BASE_URL}{MAKE_PURCHASE_OPERATION_ENDPOINT}", json=payload)
    response.raise_for_status()

    data = response.json()
    operation_id = data["operation"]["id"]
    print(f"Совершена операция покупки: operationId={operation_id}")
    return operation_id


def get_operation_receipt(client: httpx.Client, operation_id: str) -> dict:
    response = client.get(f"{BASE_URL}{OPERATION_RECEIPT_ENDPOINT}/{operation_id}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    with httpx.Client(timeout=30.0) as client:
        user_id = create_user(client)

        account_id, card_id = open_credit_card_account(client, user_id)

        operation_id = make_purchase_operation(client, account_id, card_id)

        receipt = get_operation_receipt(client, operation_id)

        print("\nЧек по операции:")
        print(receipt)


if __name__ == "__main__":
    main()