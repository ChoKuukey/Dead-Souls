import sys
import os

""" добавляет родительский каталог текущего скрипта в начало системного пути (sys.path). Это позволяет скрипту импортировать модули из родительского каталога. """
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import server.send_confirm_code

def main(email: str, code: str):
    server.send_confirm_code(email, code)
