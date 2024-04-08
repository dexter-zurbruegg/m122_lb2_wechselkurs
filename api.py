import export
import requests
import json

API_KEY = 'ae2a87ed71df46cede889e85'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/CHF'


def get_exchange_rates():
    response = requests.get(API_URL)
    data = response.json()
    return data


print(get_exchange_rates())

