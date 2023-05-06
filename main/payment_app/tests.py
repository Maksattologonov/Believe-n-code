import hashlib

import requests
from decouple import config


def calculate_pg_sig(params_dict, secret_key):
    # Сортировка параметров по алфавиту
    sorted_keys = sorted(params_dict.keys())

    # Формирование строки для хэширования
    hash_str = secret_key
    for key in sorted_keys:
        hash_str += str(params_dict[key])

    # Хэширование строки с использованием SHA-1
    sha1_hash = hashlib.sha1(hash_str.encode('utf-8'))
    pg_sig = sha1_hash.hexdigest()

    # Возврат значения хэш-суммы
    return pg_sig


params_dict = {
    "pg_merchant_id": 544891,
    "pg_amount": 1,
    "pg_currency": "KGS",
    "pg_order_id": 2,
    "pg_description": "FROM TOLOGONOV MAKSAT",
    "pg_lifetime ": 1440,
    "pg_testing_mode ": 1,
    "pg_salt": "SOMETHING"

}

sign_string = ''.join('{}{}'.format(key, params_dict[key]) for key in sorted(params_dict))

# добавление секретного ключа и вычисление хеш-суммы SHA256
sign_string += config("PAYBOX_SECRET_KEY")
signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

print(signature)
print(len(signature))
