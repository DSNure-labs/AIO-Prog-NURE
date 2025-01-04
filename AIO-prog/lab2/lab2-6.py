import requests
from bottle import route, run, request, response
from datetime import datetime, timedelta

url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
dataFile = "data.txt"

@route('/currency', method='GET')
def getCurrency():
    # отримання параметрів запиту
    param = request.query.get('param')

    # перевірка параметрів запиту
    if param not in ['today', 'yesterday']:
        response.status = 400
        return "Неправильний запит 'param' повинен бути 'today' або 'yesterday'"

    # визначення дати для запиту
    if param == 'today':
        date = datetime.now().strftime("%Y%m%d")
    elif param == 'yesterday':
        date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    # запит до апі НБУ
    try:
        apiResponse = requests.get(f"{url}?date={date}&json")
        apiResponse.raise_for_status()
        data = apiResponse.json()

        # Пошук курсу USD
        dataCurrency = next((item for item in data if item['cc'] == 'USD'), None)
        if not dataCurrency:
            response.status = 404
            return "USD курс не знайдено"

        # Формування відповіді
        formatDataCur = {"валюта": "USD", "курс": dataCurrency['rate'], "дата": dataCurrency['exchangedate']}
        response.content_type = 'application/json'
        return formatDataCur

    except requests.RequestException as exc:
        response.status = 500
        return f"Невдалося запросити запит з апі НБУ:: {str(exc)}"

@route('/savefile', method='POST')
def save_data():
    try:
        # отримання даних з тіла запиту
        data = request.body.read().decode('utf-8')

        if not data:
            response.status = 400
            return "Немає даних у запиті"

        # збереження даних у файл
        with open(dataFile, 'a', encoding='utf-8') as file:
            file.write(data)

        response.status = 200
        return "Дані збережені успішно"

    except Exception as exc:
        response.status = 500
        return f"Помилка у збереженні даних: {str(exc)}"

if __name__ == '__main__':
    run(host='localhost', port=8000)

#curl -X POST localhost:8000/savefile -d "test msg!123_=$%^&#@"