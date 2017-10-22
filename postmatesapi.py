import requests
import json

POSTMATES_KEY = "ZWZmY2RhOTItZWNjMy00ZGI2LWI5NTQtZjhkOTE0ZTA5NGQ5Og=="
CUSTOMER_ID = "cus_Kf3bMZuhfEUbQV"

def get_delivery_info (pickup_address, dropoff_address):

    url_params = {
        "pickup_address": pickup_address.replace(' ', '+'),
        "dropoff_address": dropoff_address.replace(' ', '+')
    }
    url =  "https://api.postmates.com/v1/customers/{}/delivery_quotes".format(CUSTOMER_ID)
    headers = {'Accept': 'application/json',
            'Authorization': 'Basic {}'.format(POSTMATES_KEY)}
    response = requests.post(url, data = url_params, headers=headers).json()
    if response: 
        return response
    else:
        return None