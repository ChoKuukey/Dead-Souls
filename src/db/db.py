""" Модуль для работы с базой данных PostgreSQL """

import psycopg2
import yaml

with open('../db/db_config.yaml', 'r') as settings_file:
    settings = yaml.safe_load(settings_file)

conn = psycopg2.connect(dbname=settings['dbname'], user=settings['user'], host=settings['host'], password=settings['password'])

cursor = conn.cursor()



cursor.close()
conn.close()