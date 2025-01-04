import socket

# хост, порт сервера
HOST = 'localhost'
PORT = 8000

# функція відправки файлу на сервер
def send_file(filename):
    # cтворення сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        # встановлення з'єднання з сервером
        clientSocket.connect((HOST, PORT))
        print(f"Підключено до сервера {HOST}:{PORT}")

        # надсилання ім'я файлу на сервер
        clientSocket.sendall(filename.encode('utf-8'))

        # відкриття файлу для читання у бінарному режимі
        with open(filename, 'rb') as file:
            while chunk := file.read(1024):
                clientSocket.sendall(chunk)

        print(f"Файл {filename} успішно відправлено.")

if __name__ == "__main__":
    # введення імені файлу для відправки
    file_to_send = input("Введіть шлях до файлу, який потрібно відправити: ")
    try:
        send_file(file_to_send)
    except FileNotFoundError:
        print("Файл не знайдено. Перевірте шлях і спробуйте знову.")
    except Exception as exc:
        print(f"Сталася помилка: {exc}")
