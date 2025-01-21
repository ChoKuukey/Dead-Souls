#include "../../src/server/data_func.h"

#include <stdio.h>

int main(void) {
    char* confirm_code = generate_confirm_code();
    printf(">> Confirm code: %s\n", confirm_code);
    return 0;
}