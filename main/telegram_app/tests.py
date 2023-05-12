import requests

url = "https://api.freedompay.money/init_payment.php"

payload = {'pg_order_id': '001022',
           'pg_merchant_id': '544891',
           'pg_amount': '10',
           'pg_description': 'Ticket',
           'pg_salt': 'some random string',
           'pg_sig': '768e646680def5164db7ef6fa92c7437',
           'pg_result_url': 'http://139.59.230.200:8000/success_callback',
           'pg_testing_mode': '1',
           'pg_param1': '1'}
files = [

]
headers = {

}

response = requests.request("POST", url, headers=headers, data=payload)

print(response)
print(response.text)
