import hashlib
import random
import string


def get_password_hash(string):
    input_bytes = string.encode('utf-8')

    # Выбираем алгоритм хэширования, например, SHA-256
    hash_object = hashlib.sha256()

    # Обновляем объект хэша с байтами строки
    hash_object.update(input_bytes)

    # Получаем хэш строку в формате шестнадцатеричного числа
    hashed_string = hash_object.hexdigest()
    return hashed_string


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def save_image_from_bytes(file_path, image_data):
    with open(file_path, 'wb') as file:
        image_data.seek(0)
        file.write(image_data.read())
