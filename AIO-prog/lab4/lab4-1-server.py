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
        with conn:
            print(f"Підключення від {addr}")
            while True:
                # отримання даних від клієнта
                data = conn.recv(1024)
                if not data:
                    break
                # відправка отриманих даних назад клієнту
                conn.sendall(data)
                print(f"Отримано і повернуто: {data.decode('utf-8')}")