from bottle import Bottle, request, response, run, HTTPResponse

app = Bottle()

# зберігання в пам'яті користувачів і позицій
users = {
    "admin": "password123"
}

items = {
    "1": {"name": "Еспресо", "price": 50},
    "2": {"name": "Лате", "price": 60},
    "3": {"name": "Капучино", "price": 70},
    "4": {"name": "Макіато", "price": 65},
    "5": {"name": "Американо", "price": 55},
    "6": {"name": "Флет-вайт", "price": 75}
}

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
        return {"message": "Позиція оновлена успішно."}

    elif request.method == 'DELETE':
        del items[id]
        return {"message": "Позиція видалена успішно."}

if __name__ == '__main__':
    run(app, host='localhost', port=8000, debug=True)