import socket

# хост, порт сервера
HOST = 'localhost'
PORT = 8000

# створення сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    # встановлення з'єднання з сервером
    clientSocket.connect((HOST, PORT))
    print(f"Підключено до сервера {HOST}:{PORT}")

    while True:
        # введення повідомлення для відправки серверу
        message = input("Введіть повідомлення (або 'exit' для виходу): ")
        if message.lower() == 'exit':
            print("Завершення роботи клієнта.")
            break

        # відправка повідомлення серверу
        clientSocket.sendall(message.encode('utf-8'))

        # отримання відповіді від сервера
        data = clientSocket.recv(1024)
        print(f"Відповідь від сервера: {data.decode('utf-8')}")