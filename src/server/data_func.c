#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


char* read_file(const char* filename) {
    FILE* file = fopen(filename, "rb");

    if (file == NULL) {
        fprintf(stderr, ">> failed to open file %s\n", filename);
        exit(1);
    }

    fseek(file, 0L, SEEK_END);  // move the file pointer to the end of the file
    size_t fileSize = ftell(file);  // get the current position of the file pointer
    rewind(file);  // move the file pointer back to the beginning of the file
    // printf("file size: %zu bytes\n", fileSize);

    char* buffer = (char*)malloc(fileSize+1);
    if (buffer == NULL) {
        fprintf(stderr, ">> Not enough memory to read \"%s\".\n", filename);
        exit(1);
    }

    size_t byteread = fread(buffer, sizeof(char), fileSize, file);
    // printf("bytes read: %zu\n", byteread);
    if (byteread < fileSize) {
        fprintf(stderr, ">> Could not read file \"%s\".\n", filename);
    }

    buffer[byteread] = '\0';

    fclose(file); // закрываем файл после чтения

    // printf("%s\n", buffer);

    return buffer;
}

void parse_yaml(char* yaml_string, char** config, int elements) {
    if (config == NULL || &elements <= 0) {
        fprintf(stderr, ">> Invalid arguments in parse_yaml\n");
        exit(1);
    }

    char* token = strtok(yaml_string, " :"); // создаем копию строки, чтобы strtok не модифицировал исходную строку
    int count = 0;

    char** tokens = (char**)malloc((elements * 2) * sizeof(char*));
     if (tokens == NULL) {
        fprintf(stderr, ">> Memory allocation failed\n");
        exit(1);
    }

    while (token != NULL && count < elements * 2) {
        tokens[count] = strdup(token);
        if (tokens[count] == NULL) {
            fprintf(stderr, ">> Memory allocation failed\n");
            exit(1);
        }
        token = strtok(NULL, " :\n");
        count++;
    }

    for (int i = 0; i < count; ++i) {
        if (i % 2 == 1 || i == 1) {
            config[i / 2] = tokens[i];
        }
        
    }

    free(tokens);

    if (count >= elements) {
        count -= elements;
    } else {
        count = 0;
    }
}

char** get_yaml_config(const char* src, int elements) {
    char* yaml_string = read_file(src);

    if (!yaml_string) {
        fprintf(stderr, ">> Error reading file \"%s\"\n", src);
        exit(1);
    }


    char** config = (char**)malloc(elements * sizeof(char*));
    parse_yaml(yaml_string, config, elements);

    // for (int i = 0; i < count; ++i) {
    //     printf("%s\n", config[i]);
    // }
    
    return config;
}

char** parse_data_string(const char* data_string) {
    if (data_string == NULL) {
        fprintf(stderr, ">> parse_data_string is NULL\n");
        exit(1);
    }

    char* query_copy = strdup(data_string);
    if (query_copy == NULL) {
        fprintf(stderr, ">> Not enough memory to duplicate the string.\n");
        exit(1);

    }

    char* token = strtok(query_copy, " \n"); // создаем копию строки, чтобы strtok не модифицировал исходную строку

    int count = 0;
    while (token != NULL) {
        count++;
        token = strtok(NULL, " \n");
    }

    if (count == 0) {
        fprintf(stderr, ">> No tokens found in the query string.\n");
        free(query_copy);
        exit(1);
    }

    printf(">> Count: %d\n", count);

    char** tokens = (char**)malloc((count + 1) * sizeof(char*));
    if (tokens == NULL) {
        fprintf(stderr, ">> Not enough memory to allocate tokens array.\n");
        free(query_copy);
        exit(1);
    }

    strcpy(query_copy, data_string);    // Восстановить исходную строку для токенизации
    int index = 0;
    token = strtok(query_copy, " \n");
    while (token != NULL) {
        tokens[index] = strdup(token);
        if (tokens[index] == NULL) {
            fprintf(stderr, ">> Not enough memory to duplicate token.\n");
            // Освобождаем ранее выделенную память
            for (int i = 0; i < index; i++) {
                free(tokens[i]);
            }
            free(tokens);
            free(query_copy);
            exit(1);
        }
        index++;
        token = strtok(NULL, " \n");
    }
    tokens[index] = NULL; // Добавляем NULL-терминатор в конце массива

    free(query_copy);
    return tokens;
}
