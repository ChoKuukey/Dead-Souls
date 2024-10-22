#include "data_func.h"


char* get_db_config(const char* src) {
    FILE* file = fopen(src, "r");

    if (file == NULL) {
        fprintf(stderr, ">> failed to open file db_config.yaml\n");
        exit(1);
    }

    fseek(file, 0L, SEEK_END);  // move the file pointer to the end of the file
    size_t fileSize = ftell(file);  // get the current position of the file pointer
    rewind(file);  // move the file pointer back to the beginning of the file

    char* buffer = (char*)malloc(fileSize+1);
    if (buffer == NULL) {
        fprintf(stderr, ">> Not ehoungh memory to read \"%s\".\n", src);
        exit(1);
    }

    size_t byteread = fread(buffer, sizeof(char), fileSize, file);
    if (byteread < fileSize) {
        fprintf(stderr, ">> Could not read file \"%s\".\n", src);
    }

    buffer[byteread] = '\0';

    fclose(file);
    return buffer;
}