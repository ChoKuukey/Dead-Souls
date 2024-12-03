#ifndef BD_H
#define BD_H
#endif
#if defined(_WIN32) || defined(_WIN64)
#include "D:\PostgreSQL\16\include\libpq-fe.h"
// #include "C:/Program Files/PostgreSQL/16/include/libpq-fe.h"
#else
#include "/usr/include/postgresql/libpq-fe.h"
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define CONN_INFO_SIZE 256
#define MAX_SQL_QUERY_LENGTH 1024
#define MAX_RESULT_LENGTH 256

typedef enum {
    QUERY_ERROR = 1 , // Ошбика запроса в БД
    QUERY_SUCCESS, // Успешный запрос
    QUERY_UNKNOWN, // Неизвестный статус
    QUERY_EXCEPTION // 
} QUERY_STATUS;

typedef enum {
    ACCOUNT_REGISTRATION = 0,
    ACCOUNT_SIGNIN
} QUERY_FLAGS;



void connect_to_db(void);
int account_signin(char** data_string);
uint8_t account_registration(char** data_string);