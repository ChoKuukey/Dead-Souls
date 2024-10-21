import socket
import time

def connect_to_server(server, port):
    print(">> Configuring remote address...")

    print(">> Creating socket...")

    print(">> Connecting...")

    try:
        remote_address = socket.getaddrinfo(server, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.error as e:
        print(f">> Connection failed: {e}")
        return
    
    for family, socktype, proto, canonname, sockaddr in remote_address:
        print(f">> Remote address is: {sockaddr[0]}:{sockaddr[1]}")

    print(">> Creatings socket...")

    try:
        socket_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f">> socket() failed. ({e})")
        return
    
    print(">> Connecting...")

    try:
        socket_peer.connect(remote_address[0][4])
    except socket.error as e:
        print(f">> connect() failed. ({e})")
        return
    
    print(">> Connected.")
    
    return socket_peer


def close_connection_to_server(socket_peer):
    print("Closing socket...")
    socket_peer.close()
    print("Finished.")
