import hashlib

import requests

from decouple import config

params = {
    'pg_order_id': 12131223,
    'pg_merchant_id': 544891,
    'pg_amount': 1,
    'pg_description': 'FROM',
    'pg_salt': 'som',
    'pg_result_url': 'http://139.59.230.200:8000/success_callback',
    'pg_testing_mode': 1
}

secret_key = 'UPNbPW1IE8yTg0W2'

sorted_params = sorted(params.items(), key=lambda x: x[0])

# Конкатенация значений параметров
concatenated_params = ';'.join([f'{value}' for key, value in sorted_params])
# Добавление секретного ключа в конец строки
concatenated_params += f';{secret_key}'
concatenated_param1 = '/init_payment.php;' + concatenated_params
# Вычисление MD5 хеша
signature = hashlib.md5(concatenated_param1.encode()).hexdigest()

# Добавление подписи к параметрам
params['pg_sig'] = signature
print(concatenated_param1)
response = requests.post('https://api.freedompay.money/init_payment.php', data=params,
                         headers={'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>'})
if response.status_code == 200:
    print(response.text)
    print(response.request.body)
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)