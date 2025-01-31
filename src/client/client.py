""" Модуль для работы с сервером """

import socket
import select
import time
import os
import sys
import pygame
import threading

from widgets.label import Label

from scenes.MainGameScrene import MainGameScene
from scenes.singin import SignInScene
from scenes.register import Register_Scene
from scenes.ConfirmCodeScene import ConfirmCode_scene

""" добавляет родительский каталог текущего скрипта в начало системного пути (sys.path). Это позволяет скрипту импортировать модули из родительского каталога. """
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data.dataFuncs import parse_yaml_config

pygame.init()

fpsClock = pygame.time.Clock()

class Client:
    def __init__(self):
        self.run = True
        self.socket_peer = None
        self.recv_data = None

    def connect_to_server(self, server, port):
        try:
            remote_address = socket.getaddrinfo(server, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        except socket.error as e:
            print(f">> Connection failed: {e}")
            return

        for family, socktype, proto, canonname, sockaddr in remote_address:
            print(f">> Remote address is: {sockaddr[0]}:{sockaddr[1]}")

        print(">> Creatings socket...")

        try:
            self.socket_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_peer.setblocking(False)  # Set socket to non-blocking mode
        except socket.error as e:
            print(f">> socket() failed. ({e})")
            return

        print(">> Connecting...")

        try:
            self.socket_peer.connect(remote_address[0][4])
            print(">> Connected.")
        except BlockingIOError:
            pass  # Non-blocking connect will raise this error initially

        print(">> Waiting for data...")
        # Main loop where we wait for data to be received from the server
        while self.run:
            # Use select() to wait for data to be available on the socket_peer
            # select() takes three lists of sockets as arguments: the first
            # for read readiness, the second for write readiness, and the third
            # for exceptional conditions. We only care about read readiness here.
            # The fourth argument is a timeout, which we set to 0.5 seconds.
            ready_to_read, _, _ = select.select([self.socket_peer], [], [], 0.5)

            # If there is data to be read from the socket_peer
            if ready_to_read:
                try:
                    # Try to receive data from the socket_peer
                    self.recv_data = self.socket_peer.recv(1024)

                    # If we received some data
                    if self.recv_data:
                        # Print out the received data and its length
                        print(f">> Received: {self.recv_data.decode('utf-8')} len: {len(self.recv_data.decode('utf-8'))}")

                        # Во время регистрации, ждём подтверждения кода регистрации
                        # Костыль
                        if len(str(self.recv_data.decode('utf-8'))) == 9 and int(str(self.recv_data.decode('utf-8'))[7:9]) == 30:
                            print(">> Запуск сцены подтверждения кода регистрации")
                            # self.__run_confirm_code_scene(str(self.recv_data.decode('utf-8')))
                    else:
                        # If we didn't receive any data, print a message and return
                        print(">> No data received.")
                        return
                except socket.error as e:
                    # If there was an error receiving data, print an error message
                    # and return
                    print(f">> recv() failed. ({e})")
                    return

        if self.socket_peer is not None:
            print("Closing socket...")
            self.socket_peer.close()
            print("Finished.")
        else:
            print("Socket is not connected.")

    def close_connection_to_server(self):
        self.run = False
    
    def account_enter(self, email: str, password: str, error_label: Label, signin_scene: SignInScene, scene_params: list) -> None:
        """ Метод для авторизации пользователя """
        response_flags = parse_yaml_config("../src/client/flags.yaml")
        operation_flag = parse_yaml_config("../src/client/server_flags.yaml")
        account_enter_flag = operation_flag["account_enter"]

        query_string = f"{email} {password} {account_enter_flag}"
        try:
            send_data = self.socket_peer.send(query_string.encode("utf-8"))
        except socket.error as e:
            print(f">> Failed to send data to server. ({e})")
            error_label.set_text("Ошибка 503")
            return 

        if send_data:
            print(f">> Sent: '{query_string}' to server to autorization operation, size sent data: {send_data}")
            time.sleep(0.2)
            # print(f'recv_data = {self.recv_data.decode("utf-8")}={"str" if isinstance(self.recv_data.decode("utf-8"), str) else "int"}')
            # Ошибка
            if int(self.recv_data.decode("utf-8")) == response_flags["ERROR"]:
                error_label.set_text("Ошибка")
                return
            # Пользователь найден
            elif int(self.recv_data.decode("utf-8")) == response_flags["OK"]:
                print(">> Авторизация прошла успешно")
                signin_scene.run = False
                main_game_scene = MainGameScene(screen=scene_params[0], settings=scene_params[1], client=scene_params[2], db=scene_params[3], db_config=scene_params[4], bg=scene_params[5])
                main_game_scene.main()
            # Пользователь не найден
            elif int(self.recv_data.decode("utf-8")) == response_flags["EXCEPTION"]:
                error_label.set_text("Неверный логин или пароль")
                return
        else:
            print(">> No data sent.")
            error_label.set_text("Не удалось выполнить запрос: code -1")
            return
    def __run_confirm_code_scene(self, email: str, sent_code: str, scene_params: list) -> None:
            confirm_code_scene = ConfirmCode_scene(
                screen=scene_params[0], 
                settings=scene_params[1], 
                client=scene_params[2], 
                db=scene_params[3], 
                db_config=scene_params[4], 
                bg=scene_params[5], 
                sent_code=sent_code, 
                email=email
            )
            confirm_code_scene.main()

    def account_registration(self, email: str, name: str, password: str, error_label: Label, register_scene: Register_Scene, scene_params: list) -> None:
        """ Метод для регистрации пользователя """
        response_flags = parse_yaml_config("../src/client/flags.yaml")
        operation_flags = parse_yaml_config("../src/client/server_flags.yaml")
        account_enter_flag = operation_flags["account_register"]
        registration_flags = parse_yaml_config("../src/client/registration_flags.yaml")

        if email == "" or name == "" or password == "":
            error_label.set_text("Поля не могут быть пустыми")
            return

        query_string = f"{email} {name} {password} {account_enter_flag}"
        try:
            send_data = self.socket_peer.send(query_string.encode("utf-8"))
        except socket.error as e:
            print(f">> Failed to send data to server. ({e})")
            error_label.set_text("Ошибка 503")
            return 

        if send_data:
            print(f">> Sent: '{query_string}' to server to registration operation, size sent data: {send_data}")
            time.sleep(0.2)

            # Почта существует
            if int(self.recv_data.decode("utf-8")) == registration_flags["EMAIL_EXIST"]:
                error_label.set_text("Почта уже занята")
                return
            elif int(self.recv_data.decode("utf-8")) == registration_flags["UNCORRECT_EMAIL"]:
                error_label.set_text("Неверный формат почты")
                return
            elif int(self.recv_data.decode("utf-8")) == registration_flags["EMAIL_TOO_LONG"]:
                error_label.set_text("Почта должна быть < 30 символов")
                return
            # Имя существует
            elif int(self.recv_data.decode("utf-8")) == registration_flags["NAME_EXIST"]:
                error_label.set_text("Имя уже занято")
                return
            # Неверное имя
            elif int(self.recv_data.decode("utf-8")) == registration_flags["UNCORRECT_NAME"]:
                error_label.set_text("Имя должно быть > 3 и < 20 символов")
                return
            # Неверный пароль
            elif int(self.recv_data.decode("utf-8")) == registration_flags["UNCORRECT_PASSWORD"]:
                error_label.set_text("Пароль должен быть > 8 и < 35 символов")
                return
            elif int(self.recv_data.decode("utf-8")) == response_flags["OK"]:
                print(">> Регистрация прошла успешно")
                # Запрос на код подтверждения
                query_string = f"{email} {operation_flags['query_confirm_code']}"

                try:
                    send_data = self.socket_peer.send(query_string.encode("utf-8"))
                except socket.error as e:
                    print(f">> Failed to send data to server. ({e})")
                    return 
                
                if send_data:
                    print(f">> Sent: '{query_string}' to server to registration operation, size sent data: {send_data}")
                        
            elif int(self.recv_data.decode("utf-8")) == response_flags["ERROR"]:
                print(">> Неизвестная ошибка")
                error_label.set_text("Неизвестная ошибка")
                return   
                
                
        else:
            print(">> No data sent.")
            error_label.set_text("Не удалось выполнить запрос: code -1")
            return

    def activate_user_account(self, user_email: str, confirm_code_scene: ConfirmCode_scene, error_label: Label, scene_params: list):
        """ Активация аккаунта """
        response_flags = parse_yaml_config("../src/client/flags.yaml")
        operation_flags = parse_yaml_config("../src/client/server_flags.yaml")

        query_string = f"{user_email} {operation_flags['account_activation']}"

        try:
            send_data = self.socket_peer.send(query_string.encode("utf-8"))
        except socket.error as e:
            print(f">> Failed to send data to server. ({e})")
            error_label.set_text("Ошибка 503")
            return
        
        if send_data:
            print(f">> Sent: '{query_string}' to server to registration operation, size sent data: {send_data}")

            time.sleep(0.5)

            print(f">> Recieved data from server: {self.recv_data.decode('utf-8')} size: {len(self.recv_data.decode('utf-8'))}")

            # Ошибка
            if int(self.recv_data.decode("utf-8")) == response_flags["ERROR"]:
                print(">> Неизвестная ошибка")
                return
            elif int(self.recv_data.decode("utf-8")) == response_flags["OK"]:
                print(">> Активация прошла успешно")


                confirm_code_scene.run = False

                maim_game_scene = MainGameScene(scene_params[0], scene_params[1], self, scene_params[2], scene_params[3], "../src/imgs/main_bg.png")
                maim_game_scene.main()

        else:
            print(">> No data sent.")
            error_label.set_text("Не удалось выполнить запрос: code -1")
            return