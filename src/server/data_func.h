#ifndef DATA_FUNC_H
#define DATA_FUNC_H
#endif


char** get_yaml_config(const char* src);
void parse_yaml(char* yaml_string, char** values, int* count);
char* read_file(const char* filename);