#include "common.h"
#include <ctype.h>


int main(void) {
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

    printf(">> Creating socket...\n");
    SOCKET socket_listen;
    socket_listen = socket(bind_address->ai_family, bind_address->ai_socktype, bind_address->ai_protocol);
    if (!ISVALIDSOCKET(socket_listen)) {
        fprintf(stderr, ">> socket() failed. (%d)\n", GETSOCKETERRNO());
        exit(1);
    }
}