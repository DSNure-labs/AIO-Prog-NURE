from bottle import route, run, request

@route('/currency', method='GET') # обробка запиту GET
def getСurrency():
    # отримання параметрів запиту
    today = request.query.get('today')
    key = request.query.get('key')

    # перевірка параметрів запиту
    if today is not None and key is not None:
        return "USD - 41.5"
    else:
        return "Invalid request: missing 'today' or 'key' parameter"

if __name__ == '__main__':
    run(host='localhost', port=8000)
