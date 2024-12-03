#ifndef DATA_FUNC_H
#define DATA_FUNC_H
#endif


char** get_yaml_config(const char* src, int elements);
void parse_yaml(char* yaml_string, char** config, int elements);
char* read_file(const char* filename);
char** parse_data_string(const char* parse_data_string);