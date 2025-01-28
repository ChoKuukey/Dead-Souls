""" Модуль для работы с сервером """

import socket
import time
import os
import sys

from widgets.label import Label

from scenes.MainGameScrene import MainGameScene
from scenes.singin import SignInScene
from scenes.ConfirmCodeScene import ConfirmCode_scene

""" добавляет родительский каталог текущего скрипта в начало системного пути (sys.path). Это позволяет скрипту импортировать модули из родительского каталога. """
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data.dataFuncs import parse_yaml_config

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
        except socket.error as e:
            print(f">> socket() failed. ({e})")
            return

        print(">> Connecting...")

        try:
            self.socket_peer.connect(remote_address[0][4])
        except socket.error as e:
            print(f">> connect() failed. ({e})")
            return

        print(">> Connected.")

        while self.run:
            print(">> Waiting for data...")
            self.recv_data = self.socket_peer.recv(1024)
            if self.recv_data:
                print(f">> Received: {self.recv_data.decode('utf-8')}")
            else:
                print(">> No data received.")
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
    
    def account_registration(self, email: str, name: str, password: str, error_label: Label, signin_scene: SignInScene, scene_params: list) -> None:
        """ Метод для регистрации пользователя """
        response_flags = parse_yaml_config("../src/client/flags.yaml")
        operation_flags = parse_yaml_config("../src/client/server_flags.yaml")
        account_enter_flag = operation_flags["account_register"]
        registration_flags = parse_yaml_config("../src/client/registration_flags.yaml")
        print(registration_flags)

        if email == "" or name == "" or password == "":
            error_label.set_text("Поля не могут быть пустыми")
            return

        confirm_code = None

        query_string = f"{email} {name} {password} {account_enter_flag}"
        try:
            send_data = self.socket_peer.send(query_string.encode("utf-8"))
        except socket.error as e:
            print(f">> Failed to send data to server. ({e})")
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
            # Имя существует
            elif int(self.recv_data.decode("utf-8")) == registration_flags["NAME_EXIST"]:
                error_label.set_text("Имя уже занято")
                return
            # Неверное имя
            elif int(self.recv_data.decode("utf-8")) == registration_flags["UNCORRECT_NAME"]:
                error_label.set_text("Имя должно быть > 3 и < 50 символов")
                return
            # Неверный пароль
            elif int(self.recv_data.decode("utf-8")) == registration_flags["UNCORRECT_PASSWORD"]:
                error_label.set_text("Пароль должен быть > 8 и < 100 символов")
                return
            elif int(self.recv_data.decode("utf-8")) == response_flags["OK"]:
                print(">> Регистрация прошла успешно")
                try:
                    self.socket_peer.send(str(operation_flags["query_confirm_code"]).encode("utf-8"))
                except socket.error as e:
                    print(f">> Failed to send data to server. ({e})")
                    return

                signin_scene.run = False
                confirm_code_scene = ConfirmCode_scene(screen=scene_params[0], settings=scene_params[1], 
                                                        client=scene_params[2], db=scene_params[3], db_config=scene_params[4], bg=scene_params[5], sent_code="123", email=email)
                
                # Запрос на код подтверждения
                try:
                    send_data = self.socket_peer.send(str(operation_flags["query_confirm_code"]).encode("utf-8"))
                except socket.error as e:
                    print(f">> Failed to send data to server. ({e})")
                    return 
                
                if send_data:
                    print(f">> Sent: '{operation_flags['query_confirm_code']}' to server to registration operation, size sent data: {send_data}")
                    time.sleep(0.2)

                    # Ошибка
                    

                confirm_code_scene.main()
            elif int(self.recv_data.decode("utf-8")) == response_flags["ERROR"]:
                print(">> Неизвестная ошибка")
                error_label.set_text("Неизвестная ошибка")
                return   
                
        else:
            print(">> No data sent.")
            error_label.set_text("Не удалось выполнить запрос: code -1")
            return

