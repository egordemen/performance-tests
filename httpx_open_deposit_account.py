import time
import httpx


BASE_URL = "http://localhost:8003"

USERS_ENDPOINT = "/api/v1/users"
OPEN_DEPOSIT_ACCOUNT_ENDPOINT = "/api/v1/accounts/open-deposit-account"


def create_user(client: httpx.Client) -> dict:
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

    return response.json()


def open_deposit_account(client: httpx.Client, user_id: str) -> httpx.Response:
    payload = {
        "userId": user_id,
    }

    return client.post(f"{BASE_URL}{OPEN_DEPOSIT_ACCOUNT_ENDPOINT}", json=payload)


def main() -> None:
    with httpx.Client(timeout=30.0) as client:
        user_response = create_user(client)
        user = user_response["user"]
        user_id = user["id"]
        print(f"Создан пользователь: id={user_id}, email={user.get('email')}")

        response = open_deposit_account(client, user_id)

        print("\n=== Ответ от сервера (депозитный счёт) ===")
        print(f"Статус-код: {response.status_code}")
        print("JSON-ответ:")
        print(response.json())


if __name__ == "__main__":
    main()