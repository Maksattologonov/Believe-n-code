import hashlib
import xml.etree.ElementTree as ET
import requests

import locale
from datetime import datetime, timedelta


def build_paybox_signature(params, secret_key):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    concatenated_params = ';'.join([f'{value}' for key, value in sorted_params])
    concatenated_params += f';{secret_key}'
    concatenated_param1 = 'init_payment.php;' + concatenated_params
    signature = hashlib.md5(concatenated_param1.encode()).hexdigest()
    params['pg_sig'] = signature
    response = requests.request("POST", 'https://api.freedompay.money/init_payment.php',
                                data=params, files=[])
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        if root.find('pg_status').text == 'ok':
            pg_redirect_url = root.find('pg_redirect_url').text
            return pg_redirect_url
    else:
        print('Ошибка при отправке запроса:', response.status_code, response.text)


def convert_and_subtract_hours(time_str, hours_to_subtract):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    new_time = dt - timedelta(hours=hours_to_subtract)
    formatted_new_time = new_time.strftime('%d-%m-%Y %H:%M:%S')
    return formatted_new_time
