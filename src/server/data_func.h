#ifndef DATA_FUNC_H
#define DATA_FUNC_H
#endif


char** get_db_config(const char* src);
static void parse_yaml(char* yaml_string, char** values, int* count);
static char* read_file(const char* filename);