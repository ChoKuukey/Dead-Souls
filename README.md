# Dead-Souls 

***Не использовать Python модуль "db". Не актуальный и не используется. Использовался для временной заглушки.***




## ***__ИСПОЛЬЗОВАНИЕ__***

### Windows
+ Зайти в bin 
+ Настроить data/db/db_config.yaml со своими данными
+ Настроить LIBPQ_LINK в __*makefile*__
+ Настроить подключене libpq-fe.h в src/server/db.h
+ Собрать сервер через make: __*make win*__
+ Запустить Posqtgresql/PgAdmin
+ Настроить src/server/server.yaml со своими значениями
+ Запустить серве: __*./server.exe*__
+ Запустить игру

### Unix
+ Зайти в bin
+ Настроить data/db/linux_db_config.yaml со своими данными
+ Настроить LIBPQ_LINK в __*makefile*__
+ Настроить подключене libpq-fe.h в src/server/db.h
+ Собрать сервер через make: __*make linux*__
+ Запустить Posqtgresql: 
1. sudo service postgresql start
2. sudo service postgresql status
3. sudo -u __*your_psql_user*__ psql
4. \c __*your_psql_database*__ 
+ Настроить src/server/server.yaml со своими значениями
+ Запустить серве: __*./linux_server*__
+ Запустить игру