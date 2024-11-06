#include "common.h"
#include <ctype.h>
#include "db.h"


int main(void) {
    connect_to_db();
    
    #if defined(_WIN32) || defined(_WIN64)
        WSADATA d;
        if (WSAStartup(MAKEWORD(2, 2), &d)) {
            fprintf(stderr, ">> Error WinSock initialization.\n");
            exit(1);
        }
    #endif


    printf(">> Configuring server address...\n");
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE; // Режим прослушивания

    struct addrinfo *bind_address;
    getaddrinfo(0, "8080", &hints, &bind_address);

    // Слушащий сокет
    printf(">> Creating socket...\n");
    SOCKET socket_listen;
    socket_listen = socket(bind_address->ai_family, bind_address->ai_socktype, bind_address->ai_protocol);
    if (!ISVALIDSOCKET(socket_listen)) {
        fprintf(stderr, ">> socket() failed. (%d)\n", GETSOCKETERRNO());
        exit(1);
    }

    printf(">> Binding socket to local address...\n");
    if (bind(socket_listen, 
            bind_address->ai_addr, bind_address->ai_addrlen)) {
        fprintf(stderr, ">> bind() failed. (%d)\n", GETSOCKETERRNO());
        exit(1);
    }
    freeaddrinfo(bind_address);


    printf(">> Listening...\n");
    if (listen(socket_listen, 10) < 0) {
        fprintf(stderr, ">> listen() failed. (%d)\n", GETSOCKETERRNO());
        return 1;
    }

    fd_set master;
    FD_ZERO(&master);
    FD_SET(socket_listen, &master);
    SOCKET max_socket = socket_listen;

    printf(">> Waiting for connections...\n");

    while(1) {
        fd_set reads;
        reads = master;
        if (select(max_socket+1, &reads, 0, 0, 0) < 0) {
            fprintf(stderr, ">> select() failed. (%d)\n", GETSOCKETERRNO());
            return 1;
        }

        SOCKET i;
        for(i = 1; i <= max_socket; ++i) {
            if (FD_ISSET(i, &reads)) {

                if (i == socket_listen) {
                    struct sockaddr_storage client_address;
                    socklen_t client_len = sizeof(client_address);
                    SOCKET socket_client = accept(socket_listen,
                            (struct sockaddr*) &client_address,
                            &client_len);
                    if (!ISVALIDSOCKET(socket_client)) {
                        fprintf(stderr, ">> accept() failed. (%d)\n",
                                GETSOCKETERRNO());
                        return 1;
                    }

                    FD_SET(socket_client, &master);
                    if (socket_client > max_socket)
                        max_socket = socket_client;

                    char address_buffer[100];
                    getnameinfo((struct sockaddr*)&client_address,
                            client_len,
                            address_buffer, sizeof(address_buffer), 0, 0,
                            NI_NUMERICHOST);
                    printf(">> New connection from %s\n", address_buffer);
                } else {
                    // Проверка на то, был ли пользователь отключен от сервера
                    // SOCKET client_socket = i;
                    // struct sockaddr_storage client_address;
                    // socklen_t client_len = sizeof(client_address);
                    // char address_buffer[100];
                    // getnameinfo((struct sockaddr*)&client_address,
                    //             client_len,
                    //             address_buffer, sizeof(address_buffer), 0, 0,
                    //             NI_NUMERICHOST);

                    char buffer[MAX_RECV_DATA_SIZE];
                    int bytes_received = recv(i, buffer, MAX_RECV_DATA_SIZE, 0);
                    if (bytes_received == 0) {
                        printf(">> Client %d disconnected.\n", i);
                        FD_CLR(i, &master);
                        CLOSESOCKET(i);
                        continue;
                    }

                    printf(">> Client %d send: %s\n", i, buffer);

                    
                } // (i == socket_listen)
            } //if FD_ISSET
        } //for i to max_socket
    } // while(1)

    printf(">> Closing listening socket...\n");
    CLOSESOCKET(socket_listen);

    #if defined(_WIN32)
    WSACleanup();
    #endif


    printf(">> Finished.\n");

    return 0;
}   

