#include "db.h"
#include "data_func.h"


void connect_to_db(void) {
    char** db_config = get_db_config("../data/db/db_config.yaml");
    for (int i = 0; i < 6; ++i) {
        free(db_config[i]);
    }
    free(db_config);

    // Подключение к БД
    // const char* conninfo = "host=localhost port=5432 dbname=postgres user=postgres password=12345";
}