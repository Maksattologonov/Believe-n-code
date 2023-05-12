import hashlib
import xml.etree.ElementTree as ET
import requests


def build_paybox_signature(params, secret_key):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    concatenated_params = ';'.join([f'{value}' for key, value in sorted_params])
    concatenated_params += f';{secret_key}'
    concatenated_param1 = 'init_payment.php;' + concatenated_params
    signature = hashlib.md5(concatenated_param1.encode()).hexdigest()
    params['pg_sig'] = signature

    response = requests.post('https://api.freedompay.money/init_payment.php', data=params,
                             headers={
                                 'Cookie': '__cf_bm=RFP_MrdA8dgHnsAesnAObP_YHcaAcCFYKmyBGL4mKEU-1683876794-0-AVDWVEBu9ZWIj6RNIIF/h+jWgDqGGJ9ebPRmhFTpbKGlUnnnea5tbzKxUWSnSwCQJP4SDGvGNxw1NU6jVvVkAJI='})
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        print(response.text)
        pg_redirect_url = root.find('pg_redirect_url').text
        return pg_redirect_url
    else:
        print('Ошибка при отправке запроса:', response.status_code, response.text)
