import time
import httpx

unique_email = f"user_{int(time.time())}@example.com"
payload = {
    "email": unique_email,
    "lastName": "Testov",
    "firstName": "Test",
    "middleName": "Testovich",
    "phoneNumber": "+79990000000",
}
user_response = httpx.post("http://localhost:8003/api/v1/users", json=payload)
user_response.raise_for_status()
user_id = user_response.json()["user"]["id"]

deposit_payload = {"userId": user_id}
response = httpx.post("http://localhost:8003/api/v1/accounts/open-deposit-account", json=deposit_payload)
response.raise_for_status()

print("Статус-код:", response.status_code)
print("JSON-ответ:")
print(response.json())
