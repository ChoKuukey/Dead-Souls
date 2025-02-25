import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.3.123", 8623))
    
    try:
        while True:
            # Получение сообщения от сервера
            message = client.recv(1024).decode()
            print(message)
            
            # Ввод хода
            move = input("Ваш ход: ").lower()
            client.send(move.encode())
            
            # Получение ответа (ожидание или результат)
            response = client.recv(1024).decode()
            print(response)
            
            if "вышли" in response or "завершена" in response:
                break
    
    except ConnectionResetError:
        print("Сервер отключился. Игра завершена.")
    
    finally:
        client.close()


main()