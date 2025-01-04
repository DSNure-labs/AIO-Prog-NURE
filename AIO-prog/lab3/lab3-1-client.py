import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "password123"

def getItems():
    response = requests.get(f"{BASE_URL}/items", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Каталог:", response.json())
    else:
        print("Не вдалося отримати позицію. Status Code:", response.status_code, "Response:", response.json())

def addItem(item_id, name, price):
    payload = {
        "id": item_id,
        "name": name,
        "price": price
    }
    response = requests.post(f"{BASE_URL}/items", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        print("Позиція додана успішно.")
    else:
        print("Не вдалося додати позицію. Status Code:", response.status_code, "Response:", response.json())

def updateItem(item_id, name=None, price=None):
    payload = {}
    if name:
        payload["name"] = name
    if price:
        payload["price"] = price

    response = requests.put(f"{BASE_URL}/items/{item_id}", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Позиція оновлена успішно.")
    else:
        print("Не вдалося оновити позицію. Status Code:", response.status_code, "Response:", response.json())

def deleteItem(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Позиція видалена успішно.")
    else:
        print("Не вдалося видалити позицію. Status Code:", response.status_code, "Response:", response.json())

if __name__ == "__main__":
    print("Отримання всіх позицій:")
    getItems()

    print("\nДодавання нової позиції:")
    addItem("7", "Мока", 80)

    print("\nОтримання всіх позицій:")
    getItems()

    print("\nОновлення позиції:")
    updateItem("7", name="Темна Мока", price=85)

    print("\nОтримання всіх позицій:")
    getItems()

    print("\nВидалення позиції:")
    deleteItem("7")

    print("\nОтримання всіх позицій:")
    getItems()
