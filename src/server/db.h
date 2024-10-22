#ifndef BD_H
#define BD_H
#endif

#if defined(_WIN32) || defined(_WIN64)

#include "D:\PostgreSQL\16\include\libpq-fe.h"

#else

#include "/usr/include/postgresql/libpq-fe.h"

#endif

#include <stdio.h>
#include <stdlib.h>

void connect_to_db(void);