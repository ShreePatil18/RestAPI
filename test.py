import requests
import json

BASE_URL = "http://127.0.0.1:5000"  # URL of your Flask API


def register_user(name, email, phone, password):
    url = f"{BASE_URL}/users/register"
    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }
    response = requests.post(url, json=payload)
    print(f"Register response: {response.status_code} - {response.json()}")
    return response.json()

def login_user(phone, password):
    url = f"{BASE_URL}/users/login"
    payload = {
        "phone": phone,
        "password": password
    }
    response = requests.post(url, json=payload)
    print(f"Login response: {response.status_code} - {response.json()}")
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def search_user(phone, token):
    url = f"{BASE_URL}/users/search"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"phone": phone}
    response = requests.get(url, json=payload, headers=headers)
    print(f"Search response: {response.status_code} - {response.json()}")
    return response.json()

def mark_as_spam(phone, token):
    url = f"{BASE_URL}/users/addspam"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"phone": phone}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Mark as spam response: {response.status_code} - {response.json()}")
    return response.json()

if __name__ == "__main__":

    user1 = register_user("Rajesh", "Rajesh@example.com", "1234567899", "password123")
    user2 = register_user("Raju", "Raju@example.com", "0987654367", "password123")
   
    token1 = login_user("1234567899", "password123")
    token2 = login_user("0987654367", "password123")

    if token1 and token2:
 
        print("\nSearching for Rajesh (1234567899):")
        search_user("1234567899", token1)

        print("\nSearching for Raju (0987654367):")
        search_user("0987654367", token1)

        print("\nMarking Raju's number as spam by Rajesh:")
        mark_as_spam("0987654367", token1)

        print("\nSearching for Raju after marking as spam:")
        search_user("0987654367", token1)
