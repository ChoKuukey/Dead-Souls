import yaml


#
##########################################
# Полуение настроек
def get_settings(src: str) -> dict:
    try:
        with open(src) as settings_file:
            return yaml.load(settings_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(">> Не удалось открыть файл settings.yaml")

def get_db_config(src: str) -> dict:
    """ Открытие файла db_config.yaml """
    try:
        with open(src) as settings_file:
            return yaml.load(settings_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(">> Не удалось открыть файл db_config.yaml")

def parse_yaml_config(src: str) -> dict:
    try:
        with open(src) as settings_file:
            return yaml.load(settings_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(">> Не удалось открыть файл f{src}")
#
###########################################
#