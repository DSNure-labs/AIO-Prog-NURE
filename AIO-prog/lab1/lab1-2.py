import requests
from datetime import datetime, timedelta

def getExchange():
    # функція для отримання курсу валют за попередній тиждень
    dateToday = datetime.today()
    dateStart = dateToday - timedelta(days=7) # обчислюємо дату 7 днів тому
    dateStartStr = dateStart.strftime('%Y%m%d') # форматуємо дати в потрібний формат (YYYYMMDD)
    dateEndStr = dateToday.strftime('%Y%m%d')
    url = "https://bank.gov.ua/NBU_Exchange/exchange_site" # параметри запиту
    params = {
        'start': dateStartStr,
        'end': dateEndStr,
        'valcode': 'usd',
        'sort': 'exchangedate',
        'order': 'desc',
        'json': ''
    }

    response = requests.get(url, params=params) # виконуємо запит до апі

    if response.status_code == 200: # перевірка на отримання даних
        data = response.json() # розбираємо дані json
        for entry in data:
            print(f"Дата: {entry['exchangedate']}, Курс: {entry['rate']} {entry['cc']}")
    else:
        print("Не вдалося отримати дані. Статус помилки:", response.status_code)

getExchange()  # викликаємо функцію
