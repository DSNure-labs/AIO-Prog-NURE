import socket

# хост, порт
HOST = 'localhost'
PORT = 8000

# створення сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    # прив'язка сокета до хоста і порту
    serverSocket.bind((HOST, PORT))
    # перехід у режим прослуховування
    serverSocket.listen()
    print(f"Сервер запущено на {HOST}:{PORT}")

    while True:
        # прийняття вхідного з'єднання
        conn, addr = serverSocket.accept()
        print(f"Підключено до {addr}")

        with conn:
            # очікування отримання імені файлу
            filename = conn.recv(1024).decode('utf-8')
            print(f"Отримано запит на збереження файлу: {filename}")

            # відкриття файл для запису
            with open(filename, 'wb') as file:
                while True:
                    # Отримання даних від клієнта
                    data = conn.recv(1024)
                    if not data:
                        break
                    file.write(data)

            print(f"Файл {filename} успішно збережено.")