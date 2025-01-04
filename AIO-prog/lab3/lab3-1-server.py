import json
import os
from bottle import Bottle, request, response, run, HTTPResponse

app = Bottle()

# шляхи для файлів
userFile = "lab3-1-users.json"
itemsFile = "lab3-1-items.json"

# завантаження користувачів з файлу
def loadUsers():
    if os.path.exists(userFile):
        with open(userFile, 'r') as file:
            return json.load(file)
    return {}

# завантаження позицій з файлу
def loadItems():
    if os.path.exists(itemsFile):
        with open(itemsFile, 'r') as file:
            return json.load(file)
    return {}

# збереження позицій у файл
def save_items(items):
    with open(itemsFile, 'w') as file:
        json.dump(items, file, indent=4)

users = loadUsers()
items = loadItems()

# перевірка автентифікації
def checkAuth(username, password):
    return users.get(username) == password

def authenticate():
    message = {"error": "Необхідна автентифікація."}
    response.status = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return message

def requireAuth(func):
    def wrapper(*args, **kwargs):
        auth = request.auth
        if not auth or not checkAuth(auth[0], auth[1]):
            return authenticate()
        return func(*args, **kwargs)
    return wrapper

# endpoint для керування всіма позиціями
@app.route('/items', method=['GET', 'POST'])
@requireAuth
def itemsEp():
    if request.method == 'GET':
        return items
    elif request.method == 'POST':
        data = request.json
        item_id = data.get('id')
        if not item_id or item_id in items:
            return HTTPResponse(status=400, body={"error": "Невірна або дублююча ID позиції."})
        items[item_id] = {
            "name": data.get('name'),
            "price": data.get('price')
        }
        save_items(items)
        return HTTPResponse(status=201, body={"message": "Позиція додана успішно."})

# endpoint для керування всіма позиціями за допомогою ID
@app.route('/items/<id>', method=['GET', 'PUT', 'DELETE'])
@requireAuth
def itemDetailEp(id):
    if id not in items:
        return HTTPResponse(status=404, body={"error": "Позиція не знайдена."})

    if request.method == 'GET':
        return items[id]

    elif request.method == 'PUT':
        data = request.json
        items[id].update({
            "name": data.get('name', items[id].get('name')),
            "price": data.get('price', items[id].get('price'))
        })
        save_items(items)
        return {"message": "Позиція оновлена успішно."}

    elif request.method == 'DELETE':
        del items[id]
        save_items(items)
        return {"message": "Позиція видалена успішно."}

if __name__ == '__main__':
    # створення файлу користувача, якщо його не існує
    if not os.path.exists(userFile):
        with open(userFile, 'w') as file:
            json.dump({"admin": "password123"}, file, indent=4)

    run(app, host='localhost', port=8000, debug=True)