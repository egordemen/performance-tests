import time
import httpx

unique_email = f"user_{int(time.time())}@example.com"
user_response = httpx.post("http://localhost:8003/api/v1/users", json={
    "email": unique_email,
    "lastName": "Testov",
    "firstName": "Test",
    "middleName": "Testovich",
    "phoneNumber": "+79990000000",
})
user_response.raise_for_status()
user_id = user_response.json()["user"]["id"]

account_response = httpx.post("http://localhost:8003/api/v1/accounts/open-credit-card-account", json={
    "userId": user_id,
})
account_response.raise_for_status()
account_data = account_response.json()
account_id = account_data["account"]["id"]
card_id = account_data["account"]["cards"][0]["id"]

purchase_response = httpx.post("http://localhost:8003/api/v1/operations/make-purchase-operation", json={
    "status": "IN_PROGRESS",
    "amount": 77.99,
    "category": "taxi",
    "cardId": card_id,
    "accountId": account_id,
})
purchase_response.raise_for_status()
operation_id = purchase_response.json()["operation"]["id"]

receipt_response = httpx.get(f"http://localhost:8003/api/v1/operations/operation-receipt/{operation_id}")
receipt_response.raise_for_status()

print("Чек по операции:")
print(receipt_response.json())
