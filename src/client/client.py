""" Модуль для работы с сервером """

import socket
import time
import os
import sys

from widgets.label import Label

""" добавляет родительский каталог текущего скрипта в начало системного пути (sys.path). Это позволяет скрипту импортировать модули из родительского каталога. """
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data.dataFuncs import parse_yaml_config

class Client:
    def __init__(self):
        self.run = True
        self.socket_peer = None

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
            data = self.socket_peer.recv(1024)
            if data:
                print(f">> Received: {data.decode()}")
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

    def account_enter(self, email: str, password: str, error_label: Label) -> None:
        """ Метод для авторизации пользователя """
        flags = parse_yaml_config("../src/server/flags.yaml")
        account_enter_flag = flags["account_enter"]

        query_string = f"{email} {password} {account_enter_flag}"
        try:
            send_data = self.socket_peer.send(query_string.encode("utf-8"))
        except socket.error as e:
            print(f">> Failed to send data to server. ({e})")
            return 

        if send_data:
            print(f">> Sent: {query_string} to server to autorization operation, size sent data: {send_data}")
        else:
            print(">> No data sent.")
            return
