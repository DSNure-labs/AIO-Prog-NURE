import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def getExchange():
    # функція для отримання курсу валют за попередній тиждень
    dateToday = datetime.today()
    dateStart = dateToday - timedelta(days=7)  # обчислюємо дату 7 днів тому
    dateStartStr = dateStart.strftime('%Y%m%d')  # форматуємо дати в потрібний формат (YYYYMMDD)
    dateEndStr = dateToday.strftime('%Y%m%d')

    url = "https://bank.gov.ua/NBU_Exchange/exchange_site"
    # параметри запиту
    params = {
        'start': dateStartStr,
        'end': dateEndStr,
        'valcode': 'usd',
        'sort': 'exchangedate',
        'order': 'desc',
        'json': ''
    }

    response = requests.get(url, params=params)  # виконуємо запит до апі

    if response.status_code == 200:  # перевірка на отримання даних
        data = response.json()  # розбираємо дані json

        # списки для збереження дат і курсів
        dates = []
        rates = []

        for entry in data:
            print(f"Дата: {entry['exchangedate']}, Курс: {entry['rate']} {entry['cc']}")
            dates.append(entry['exchangedate'])  # додаємо дату до списку
            rates.append(entry['rate'])  # додаємо курс до списку

        # побудова графіку
        dates = [datetime.strptime(date, '%d.%m.%Y') for date in dates]  # перетворюємо дати в об'єкти datetime
        plt.figure(figsize=(10, 6))  # розмір графіку
        plt.plot(dates, rates, marker='o', linestyle='-', label='Курс USD')
        plt.title('Зміна курсу USD за останній тиждень')
        plt.xlabel('Дата')
        plt.ylabel('Курс (UAH)')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)  # повертаємо підписи дат
        plt.tight_layout()
        plt.show()

    else:
        print("Не вдалося отримати дані. Статус помилки:", response.status_code)

getExchange()  # викликаємо функцію