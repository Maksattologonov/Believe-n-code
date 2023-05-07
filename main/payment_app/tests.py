import hashlib
import json

import requests
from decouple import config


import hashlib

pg_merchant_id = config("PAYBOX_MERCHANT_ID")
secret_key = config("PAYBOX_SECRET_KEY")

signature = "52509e597b3bd0c496833c4f4ac237e2"

unhash = hashlib.md5(signature.encode(s))