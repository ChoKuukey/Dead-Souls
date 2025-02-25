import socket
import threading

# Список возможных ходов
moves = ["камень", "ножницы", "бумага"]

# Функция определения победителя
def determine_winner(player1_move, player2_move):
    if player1_move == player2_move:
        return "Ничья!"
    elif (player1_move == "камень" and player2_move == "ножницы") or \
         (player1_move == "ножницы" and player2_move == "бумага") or \
         (player1_move == "бумага" and player2_move == "камень"):
        return "Игрок 1 выиграл!"
    else:
        return "Игрок 2 выиграл!"

# Обработка клиента
def handle_client(client_socket, player_num, moves_dict, lock, clients_connected):
    while True:
        client_socket.send(f"Игрок {player_num}, введите ваш ход (камень, ножницы, бумага) или 'выход' для завершения: ".encode())
        move = client_socket.recv(1024).decode().lower()
        
        if move == "выход":
            with lock:
                clients_connected[player_num] = False
            client_socket.send("Вы вышли из игры. До свидания!".encode())
            return
        
        if move not in moves:
            client_socket.send("Неверный ход! Попробуйте снова.".encode())
            continue
        
        with lock:
            moves_dict[player_num] = move
            client_socket.send("Ждем второго игрока...".encode())
        
        # Ожидание, пока оба игрока сделают ход
        while len(moves_dict) < 2:
            with lock:
                if not all(clients_connected.values()):
                    client_socket.send("Один из игроков вышел. Игра завершена.".encode())
                    return
        
        # Отправка результата
        with lock:
            result = determine_winner(moves_dict[1], moves_dict[2])
            message = f"Игрок 1 выбрал: {moves_dict[1]}, Игрок 2 выбрал: {moves_dict[2]}. {result}"
            client_socket.send(message.encode())
            moves_dict.clear()  # Очистка ходов для следующего раунда

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.3.123", 8623))
    server.listen(2)
    
    print("Сервер запущен, ожидание игроков...")
    
    moves_dict = {}  # Словарь для хранения ходов
    lock = threading.Lock()  # Блокировка для синхронизации
    clients_connected = {1: True, 2: True}  # Состояние подключения игроков
    clients = []  # Список клиентских сокетов
    
    # Подключение двух игроков
    for i in range(2):
        client_socket, addr = server.accept()
        print(f"Игрок {i+1} подключился: {addr}")
        clients.append(client_socket)
        
        # Запуск потока для каждого игрока
        thread = threading.Thread(target=handle_client, args=(client_socket, i+1, moves_dict, lock, clients_connected))
        thread.start()
    
    # Ожидание завершения всех потоков
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()
    
    server.close()


main()