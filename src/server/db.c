#include "data_func.h"
#include "db.h"

PGconn *conn;



static void print_libpq_version() {
    int lib_ver = PQlibVersion();
    printf(">> Version of libpq: %d\n", lib_ver);
    
}
static void exit_nicely(PGconn *conn) {
    // Закрытие соединения
    PQfinish(conn);
}

char** get_db_config(void) {
    char** db_config;
    #if defined(_WIN32) || defined(_WIN64)
    db_config = get_yaml_config("../data/db/db_config.yaml", 6);
    #endif
    db_config = get_yaml_config("../data/db/linux_db_config.yaml", 6);
    return db_config;
}

void connect_to_db(void) {
    print_libpq_version();

    char** db_config = get_db_config();

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
    conn = PQconnectdb(conninfo);

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
        email VARCHAR(255) NOT NULL UNIQUE, \
        name VARCHAR(255) NOT NULL, \
        password_digest VARCHAR(255) NOT NULL, \
        is_dev boolean NOT NULL DEFAULT FALSE, \
        create_at timestamp without time zone, \
        updated_at timestamp without time zone, \
        is_active boolean NOT NULL DEFAULT FALSE);", db_config[4]);

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


    // Создание расширения uuid-ossp, для генерации уникальных идентификаторов
    char create_uuid_ossp_extension_on_table_sessions[MAX_SQL_QUERY_LENGTH];
    snprintf(create_uuid_ossp_extension_on_table_sessions, MAX_SQL_QUERY_LENGTH, "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";");
    PGresult *uuid_res = PQexecParams(conn, create_uuid_ossp_extension_on_table_sessions, 0, NULL, NULL, NULL, NULL, 0);
    // Проверка выполнения запроса
    if (PQresultStatus(uuid_res) != PGRES_COMMAND_OK) {
        fprintf(stderr, "Query failed:%s\n", PQerrorMessage(conn));
        PQclear(uuid_res);
        exit_nicely(conn);
        exit(1);
    }

    // Создание таблицы sessions, если её нет
    char create_sessions_table[MAX_SQL_QUERY_LENGTH];
    snprintf(create_sessions_table, MAX_SQL_QUERY_LENGTH, "CREATE TABLE IF NOT EXISTS %s ( \
        id SERIAL PRIMARY KEY, \
        user_id INTEGER NOT NULL, \
        session_id UUID NOT NULL DEFAULT uuid_generate_v4(), \
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
        online BOOLEAN NOT NULL DEFAULT FALSE, \
        CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES %s(id) ON DELETE CASCADE);", db_config[5], db_config[4]);
    // CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id));", db_config[5], db_config[4]);
    // Это определяет внешний ключ для столбца user_id, который ссылается на столбец id в таблице users.
    // Это обеспечивает целостность данных, гарантируя, что каждый user_id в текущей таблице соответствует существующему id в таблице users.
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

    // Создание индекса idx_session_id на session_id в таблице sessions, если его нет
    char create_index_session_id_on_sessions[MAX_SQL_QUERY_LENGTH];
    snprintf(create_index_session_id_on_sessions, MAX_SQL_QUERY_LENGTH, "CREATE INDEX IF NOT EXISTS idx_session_id ON sessions (session_id);");
    PGresult *index_session_id_res = PQexecParams(conn, create_index_session_id_on_sessions, 0, NULL, NULL, NULL, NULL, 0);
    // Проверка выполнения запроса
    if (PQresultStatus(index_session_id_res)!= PGRES_COMMAND_OK) {
        fprintf(stderr, "Query failed:%s\n", PQerrorMessage(conn));
        PQclear(index_session_id_res);
        exit_nicely(conn);
        exit(1);
    }

    // Создание индекса idx_user_id на user_id в таблице sessions, если его нет
    char create_index_user_id_on_sessions[MAX_SQL_QUERY_LENGTH];
    snprintf(create_index_user_id_on_sessions, MAX_SQL_QUERY_LENGTH, "CREATE INDEX IF NOT EXISTS idx_user_id ON sessions (user_id);");
    PGresult *index_user_id_res = PQexecParams(conn, create_index_user_id_on_sessions, 0, NULL, NULL, NULL, NULL, 0);
    // Проверка выполнения запроса
    if (PQresultStatus(index_user_id_res)!= PGRES_COMMAND_OK) {
        fprintf(stderr, "Query failed:%s\n", PQerrorMessage(conn));
        PQclear(index_user_id_res);
        exit_nicely(conn);
        exit(1);
    }

    for (int i = 0; i < 6; ++i) {
        free(db_config[i]);
    }
    free(db_config);

    // Подключение к БД
    // const char* conninfo = "host=localhost port=5432 dbname=postgres user=postgres password=12345";
}

int account_signin(char** data_string) {
    char** db_config = get_db_config();

    if (conn == NULL || data_string == NULL) {
        fprintf(stderr, ">> Invalid arguments in account_signin\n");
        exit(1);
    }

    const char* email = data_string[0];
    const char* password = data_string[1];

    char query[MAX_SQL_QUERY_LENGTH];
    snprintf(query, MAX_SQL_QUERY_LENGTH, "SELECT * FROM %s WHERE email = '%s' AND password_digest = '%s';", db_config[4], data_string[0], data_string[1]);

    
    PGresult* res = PQexecParams(conn, query, 0, NULL, NULL, NULL, NULL, 0);

    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        fprintf(stderr,  ">> Query failed: %s\n", PQerrorMessage(conn));
        PQclear(res);
        return QUERY_ERROR;
    }

    int rows = PQntuples(res);
    PQclear(res);

    if (rows > 0) {
        printf(">> User %s successfully signed in\n", email);
        return QUERY_SUCCESS;
    } else {
        printf(">> User %s not found\n", email);
        return QUERY_EXCEPTION;
    }
}