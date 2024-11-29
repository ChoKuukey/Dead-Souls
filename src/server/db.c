#if defined(_WIN32) || defined(_WIN64)
// #include "D:\PostgreSQL\16\include\libpq-fe.h"
#include "C:/Program Files/PostgreSQL/16/include/libpq-fe.h"
#else
#include "/usr/include/postgresql/libpq-fe.h"
#endif

#include <stdio.h>
#include <stdlib.h>
#include "data_func.h"

#define CONN_INFO_SIZE 256
#define MAX_SQL_QUERY_LENGTH 1024


static void print_libpq_version() {
    int lib_ver = PQlibVersion();
    printf(">> Version of libpq: %d\n", lib_ver);
    
}
static void exit_nicely(PGconn *conn) {
    // Закрытие соединения
    PQfinish(conn);
}

void connect_to_db(void) {
    print_libpq_version();

    char** db_config;

    #if defined(_WIN32) || defined(_WIN64)
    db_config = get_yaml_config("../data/db/db_config.yaml", 6);
    #endif
    db_config = get_yaml_config("../data/db/linux_db_config.yaml", 6);

    // for (int i = 0; i < 6; ++i) {
    //     printf(">> db_config[%d]: %s\n", i, db_config[i]);
    // }
    
    char conninfo[CONN_INFO_SIZE];   // строка конфига подключения

    snprintf(conninfo, CONN_INFO_SIZE, "host=%s port=5432 dbname=%s \
        user=%s password=%s sslmode=prefer connect_timeout=10",
        db_config[2], db_config[0], db_config[1], db_config[3]);

    conninfo[CONN_INFO_SIZE - 1] = '\0';
    // printf(">> conninfo: %s\n", conninfo);

    // Подключение к БД
    PGconn *conn = PQconnectdb(conninfo);
    

    // Проверка подключения
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
        exit(1);
    }
    puts("\n");
    printf(">> Successfully connected to database\n");
    puts("\n");

    // Создание таблицы users, если её нет
    char create_users_table[MAX_SQL_QUERY_LENGTH];
    snprintf(create_users_table, MAX_SQL_QUERY_LENGTH, "CREATE TABLE IF NOT EXISTS %s ( \
        id SERIAL PRIMARY KEY, \
        email VARCHAR(255), \
        name VARCHAR(255), \
        password_digest VARCHAR(255), \
        is_dev boolean, \
        create_at timestamp without time zone, \
        is_active boolean);", db_config[4]);

    PGresult *users_res = PQexecParams(conn, create_users_table, 0, NULL, NULL, NULL, NULL, 0);

    // Проверка выполнения запроса
    if (PQresultStatus(users_res) != PGRES_COMMAND_OK) {
        fprintf(stderr, "Query failed:%s\n", PQerrorMessage(conn));
        PQclear(users_res);
        exit_nicely(conn);
        exit(1);
    }

    printf(">> Successfully created table \"%s\" or have been already created %s\n", db_config[4], db_config[4]);
    puts("\n");

    // Создание таблицы sessions, если её нет
    char create_sessions_table[MAX_SQL_QUERY_LENGTH];
    snprintf(create_sessions_table, MAX_SQL_QUERY_LENGTH, "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; \
        CREATE TABLE IF NOT EXISTS %s ( \
        id SERIAL PRIMARY KEY, \
        user_id INTEGER NOT NULL, \
        session_id UUID NOT NULL DEFAULT uuid_generate_v4(), \
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
        online BOOLEAN NOT NULL DEFAULT FALSE, \
        CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES %s(id) \
        ); \
        CREATE INDEX IF NOT EXISTS idx_session_id ON sessions (session_id); \
        CREATE INDEX IF NOT EXISTS idx_user_id ON sessions (user_id);", db_config[5], db_config[5]);

    PGresult *session_res = PQexecParams(conn, create_sessions_table, 0, NULL, NULL, NULL, NULL, 0);

    // Проверка выполнения запроса
    if (PQresultStatus(session_res)!= PGRES_COMMAND_OK) {
        fprintf(stderr, "Query failed:%s\n", PQerrorMessage(conn));
        PQclear(session_res);
        exit_nicely(conn);
        exit(1);
    }

    printf(">> Successfully created table \"%s\" or have been already created %s\n", db_config[5], db_config[5]);
    puts("\n");


    for (int i = 0; i < 6; ++i) {
        free(db_config[i]);
    }
    free(db_config);

    // Подключение к БД
    // const char* conninfo = "host=localhost port=5432 dbname=postgres user=postgres password=12345";
}


                                                                   
                                   
                                            

                                    
                                    