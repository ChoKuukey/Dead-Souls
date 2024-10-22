""" Модуль для работы с сервером """

import socket
import time

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
