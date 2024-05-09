import hashlib


def get_password_hash(string):
    input_bytes = string.encode('utf-8')

    # Выбираем алгоритм хэширования, например, SHA-256
    hash_object = hashlib.sha256()

    # Обновляем объект хэша с байтами строки
    hash_object.update(input_bytes)

    # Получаем хэш строку в формате шестнадцатеричного числа
    hashed_string = hash_object.hexdigest()
    return hashed_string
