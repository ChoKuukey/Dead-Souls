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
} QUERY_STATUS; //* Отправляем пользователю

typedef enum {
    ACCOUNT_SIGNIN = 1,
    ACCOUNT_REGISTRATION,
    CONFIRM_CODE, //* Запрос на код подтверждения
    ACCOUNT_ACTIVATION,
    GET_ACCOUNT_NAME,
    GET_USER_CD_DISK_COUNT,
    GET_USER_FLOPPY_DISK_COUNT,
    CREATE_SESSION,
    DELETE_SESSION,
    VALIDATE_SESSION,
    UPDATE_SESSION
} QUERY_FLAGS; //* Принимаем от пользователя

typedef enum {
    EMAIL_EXIST = 5,
    UNCORRECT_EMAIL,
    EMAIL_TOO_LONG,
    NAME_EXIST,
    UNCORRECT_NAME,
    UNCORRECT_PASSWORD
} REGISTRATION_STATUS; //* Отправляем пользователю

typedef enum {
    CONFIRM_CODE_SUCCESS = 30,
} CODE_STATUS; //* Отправляем пользователю


void connect_to_db(void);
int account_signin(char** data_string);
int account_registration(char** data_string);
int send_confirm_code(char** data_string, char* code);
int account_activation(char** data_string);
char* get_account_name(char** data_string);
char* get_user_cd_disk_count(char** data_string);
char* get_user_floppy_disk_count(char** data_string);
char* create_session(char** data_string);
int delete_session(char** data_string);
int validate_session(char** data_string);
int update_session(char** data_string);