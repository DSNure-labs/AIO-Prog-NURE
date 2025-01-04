import socket

# хост, порт
HOST = 'localhost'
PORT = 8000

# cтворення сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    # прив'язка сокета до хоста і порту
    serverSocket.bind((HOST, PORT))
    # перехід у режим прослуховування
    serverSocket.listen()
    print(f"Сервер запущено на {HOST}:{PORT}")

    while True:
        # прийняття вхідного з'єднання
        conn, addr = serverSocket.accept()
        print(f"Підключення від {addr}")
        with conn:
            while True:
                try:
                    # отримання даних від клієнта
                    data = conn.recv(1024)
                    if not data:
                        print(f"Клієнт {addr} завершив з'єднання")
                        break
                    # відправка отриманих даних назад клієнту
                    conn.sendall(data)
                    print(f"Отримано і повернуто: {data.decode('utf-8')}")
                except ConnectionResetError:
                    print(f"Клієнт {addr} примусово закрив з'єднання")
                    break