# Dead-Souls 

***Не использовать Python модуль "db". Не актуальный и не используется. Использовался для временной заглушки.***




## ***__ИСПОЛЬЗОВАНИЕ__***

### Windows
+ Зайти в bin 
+ Собрать сервер через make: __*make win*__
+ Настроить data/db/db_config.yaml со своими данными
+ Запустить Posqtgresql/PgAdmin
+ Настроить src/server/server.yaml со своими значениями
+ Запустить серве: __*./server.exe*__
+ Запустить игру

### Unix
+ Зайти в bin
+ Собрать сервер через make: __*make linux*__
+ Настроить data/db/linux_db_config.yaml со своими данными
+ Запустить Posqtgresql: 
1. sudo service postgresql start
2. sudo service postgresql status
3. sudo -u __*your_psql_user*__ psql
\c __*your_psql_database*__ 
+ Настроить src/server/server.yaml со своими значениями
+ Запустить серве: __*./linux_server*__
+ Запустить игру