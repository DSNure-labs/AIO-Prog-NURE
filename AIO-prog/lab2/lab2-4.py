from bottle import route, run, request, response


@route('/currency', method='GET')
def get_currency():
    # Отримання параметрів запиту
    today = request.query.get('today')
    key = request.query.get('key')

    # Перевірка параметрів запиту
    if today is not None and key is not None:
        currency_data = {"currency": "USD", "rate": "41.5"}

        # Обробка заголовків
        content_type = request.get_header('Content-Type', '').lower()

        if content_type == 'application/json':
            response.content_type = 'application/json'
            return {"data": currency_data}

        elif content_type == 'application/xml':
            response.content_type = 'application/xml'
            xml_response = f"""
            <response>
                <currency>{currency_data['currency']}</currency>
                <rate>{currency_data['rate']}</rate>
            </response>
            """
            return xml_response

        else:
            response.content_type = 'text/plain'
            return f"Currency: {currency_data['currency']}, Rate: {currency_data['rate']}"

    else:
        response.status = 400
        return "Invalid request: missing 'today' or 'key' parameter"


if __name__ == '__main__':
    run(host='localhost', port=8000)

#curl -X GET "http://localhost:8000/currency?today=2025-01-01&key=12345" -H "Content-Type: application/xml"
#curl -X GET "http://localhost:8000/currency?today=2025-01-01&key=12345" -H "Content-Type: application/json"