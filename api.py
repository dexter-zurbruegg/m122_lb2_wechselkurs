import logging
import os
import requests
import freecurrencyapi

API_KEY = 'ae2a87ed71df46cede889e85'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/CHF'
ALT_API_KEY = 'fca_live_7LMTft5sGhrRQjdDQGGEtT8XTedjLqkyOJHztFe1'
ALT_API_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={ALT_API_KEY}'

client = freecurrencyapi.Client(ALT_API_KEY)


LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResponseFileHandler(logging.FileHandler):
    def emit(self, record):
        filename = f"{LOGS_DIR}/{record.created}.log"
        with open(filename, "a") as file:
            file.write(self.format(record) + "\n")


handler = ResponseFileHandler(filename="response.log", mode="a")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def equalize_to_chf(exchange_rates):
    chf_value = exchange_rates['CHF']
    for currency, rate in exchange_rates.items():
        exchange_rates[currency] = chf_value / rate
    exchange_rates['CHF'] = 1
    return exchange_rates


def get_exchange_rates():
    response = requests.get(API_URL)
    data = response.json()
    logger.info(f"Response: {data}")
    return data


def get_alternative_exchange_rates():
    response = requests.get(ALT_API_URL)
    data = response.json()
    logger.info(f"Response: {data}")
    return data
