#include "common.h"
#include <ctype.h>
#include <stdint.h>
#include <locale.h>
#include "db.h"
#include "data_func.h"

#if defined(_WIN32) || defined(_WIN64)
#include<windows.h>
#endif


int main(void) {
    // Set the locale to UTF-8
    setlocale(LC_ALL, "en_US.UTF-8");

    char** server_config = get_yaml_config("../server/server.yaml", 2);
    char* server_address = (char*)malloc(strlen(server_config[0]) + 1);

    if (server_address == NULL) {
        fprintf(stderr, ">> Error to allocate memory for server address\n");
        exit(1);
    }
    // strcpy(server_address, server_config[0]);
    strncpy(server_address, server_config[0], strlen(server_config[0]));
    server_address[strlen(server_config[0])-1] = '\0';

    for (int i = 0; i < 2; ++i) {
        printf(">> server_config[%d]: %s\n", i, server_config[i]);
    }

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
    hints.ai_flags = AI_PASSIVE; //AI_NUMERICHOST | AI_PASSIVE | AI_NUMERICSERV; // Режим прослушивания

    struct addrinfo *bind_address;
    int result = getaddrinfo(server_address, server_config[1], &hints, &bind_address);

    if (result != 0) {
        fprintf(stderr, ">> getaddrinfo() failed. (%d)\n", result);
        if (result == EAI_NONAME) {
            fprintf(stderr, ">> Hostname or service name not found.\n");
        } else {
            fprintf(stderr, ">> Unknown error.\n");
        }
        exit(1);
    }

    // Вывод адреса сервера
    char server_ip_address[INET_ADDRSTRLEN];
    struct sockaddr_in *addr_in = (struct sockaddr_in*) bind_address->ai_addr;
    inet_ntop(AF_INET, &(addr_in->sin_addr), server_ip_address, INET_ADDRSTRLEN);
    // htons - преобразует 16-битное целое число из хостового порядка байтов в сетевой порядок байтов.
    printf("Server address: %s:%s\n", server_ip_address, server_config[1]);

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
        for(SOCKET i = 1; i <= max_socket; ++i) {
            if (FD_ISSET(i, &reads)) {
                if (i == socket_listen) {
                    struct sockaddr_storage client_address;
                    socklen_t client_len = sizeof(client_address);
                    SOCKET socket_client = accept(socket_listen, (struct sockaddr*)&client_address, &client_len);
                    if (!ISVALIDSOCKET(socket_client)) {
                        fprintf(stderr, ">> accept() failed. (%d)\n", GETSOCKETERRNO());
                        continue;
                    }

                    FD_SET(socket_client, &master);
                    if (socket_client > max_socket)
                        max_socket = socket_client;

                    char address_buffer[100];
                    getnameinfo((struct sockaddr*)&client_address, client_len, address_buffer, sizeof(address_buffer), 0, 0, NI_NUMERICHOST);
                    printf(">> New connection from %s\n", address_buffer);
                } else {
                    struct sockaddr_storage client_address;
                    SOCKET client_socket = i;
                    socklen_t client_len = sizeof(client_address);
                    getpeername(client_socket, (struct sockaddr*)&client_address, &client_len);
                    char address_buffer[INET_ADDRSTRLEN];
                    getnameinfo((struct sockaddr*)&client_address, client_len, address_buffer, sizeof(address_buffer), 0, 0, NI_NUMERICHOST);

                    char buffer[MAX_RECV_DATA_SIZE];
                    int bytes_received = recv(client_socket, buffer, MAX_RECV_DATA_SIZE, 0);
                    if (bytes_received <= 0) {
                        printf(">> Client %s disconnected.\n", address_buffer);
                        FD_CLR(client_socket, &master);
                        CLOSESOCKET(client_socket);
                        continue;
                    }

                    buffer[bytes_received] = '\0';

                    printf(">> Client %s Received: %s\n", address_buffer, buffer);

                    // Парсим данные из запроса
                    char** data = parse_data_string(buffer);
                    uint8_t data_count = 0; // Счетчик токенов
                    for (int i = 0; data[i] != NULL; i++) {
                        printf(">> Token %d: %s\n", i, data[i]);
                        data_count++;
                    }

                    printf(">> Data count: %d\n", data_count);

                    int result;
                    char result_buffer[MAX_RESULT_LENGTH + 1];

                    if (atoi(data[data_count - 1]) == ACCOUNT_REGISTRATION) {
                        //* Регистрация пользователя
                        puts(">> Starting account registration");
                        result = account_registration(data);
                    } else if (atoi(data[data_count - 1]) == ACCOUNT_SIGNIN) {
                        //* Авторизация пользователя
                        puts(">> Starting account signin");
                        result = account_signin(data);
                    } else if (atoi(data[data_count - 1]) == ACCOUNT_ACTIVATION) {
                        //* Активация аккаунта пользователя
                        printf(">> Starting account activation. User: \n%s", data[0]);
                        result = account_activation(data);
                    } else if (atoi(data[data_count - 1]) == CONFIRM_CODE) {
                        //* Отправка кода подтверждения на почту пользователя
                        puts(">> Starting confirm code");
                        char* code = generate_confirm_code();
                        printf(">> Confrim code: %s\n", code);
                        int send_res = send_confirm_code(data, code);
                        if (send_res == QUERY_SUCCESS) {
                            snprintf(result_buffer, MAX_RESULT_LENGTH, "%s %d", code, CONFIRM_CODE_SUCCESS);
                            result_buffer[MAX_RESULT_LENGTH] = '\0';
                            if (result_buffer == NULL) {
                                fprintf(stderr, ">> Failed to allocate memory for result buffer\n");
                                continue;
                            };

                            if (send(client_socket, result_buffer, strlen(result_buffer), 0) == -1) {
                                fprintf(stderr, ">> Failed to send data to client: 'NULL RESULT'\n");
                            } else {
                                printf(">> Data sent to client %s\n", result_buffer);
                            }
                            // Sleep(200);
                            continue;
                        }
                    }
                    

                    if (result == QUERY_ERROR) {
                        fprintf(stderr, ">> Failed to send data to database: 'NULL RESULT'\n");
                        snprintf(result_buffer, MAX_RESULT_LENGTH, "%d", result);
                        if (send(client_socket, result_buffer, strlen(result_buffer), 0) == -1) {
                            fprintf(stderr, ">> Failed to send data to client: 'NULL RESULT'\n");
                        } else {
                            printf(">> Data sent to client %s\n", result_buffer);
                        }
                        continue;
                    }

                    snprintf(result_buffer, MAX_RESULT_LENGTH, "%d", result);
                    result_buffer[MAX_RESULT_LENGTH] = '\0';
                    if (result_buffer == NULL) {
                        fprintf(stderr, ">> Failed to allocate memory for result buffer\n");
                        continue;
                    };

                    if (send(client_socket, result_buffer, strlen(result_buffer), 0) == -1) {
                        fprintf(stderr, ">> Failed to send data to client: 'NULL RESULT'\n");
                    } else {
                        printf(">> Data sent to client %s\n", result_buffer);
                    }
                    
                } // else if (i == socket_listen) {
            } // if (FD_ISSET(i, &reads)) {
        } // for(SOCKET i = 1; i <= max_socket; ++i) {
    } // while(1)

    printf(">> Closing listening socket...\n");
    CLOSESOCKET(socket_listen);

    #if defined(_WIN32)
    WSACleanup();
    #endif

    free(server_address);

    printf(">> Finished.\n");

    return 0;
}   


