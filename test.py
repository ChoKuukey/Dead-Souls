def parse_data_string(data_string: str):
    """ Парсит строку данных от сервера на токены """
    tokens: list = []

    tokens = data_string.split(' ')

    return tokens


data: str = "GH4TR5 example@gmail.com 30"

tokens = parse_data_string(data)
print(len(tokens))
