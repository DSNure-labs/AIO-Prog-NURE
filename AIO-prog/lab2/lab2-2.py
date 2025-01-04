from bottle import route, run

@route('/', method='GET') # обробка запиту GET
def hello():
    return "Hello World!"

if __name__ == '__main__':
    run(host='localhost', port=8000)
