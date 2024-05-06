import logging
import os
import requests
import freecurrencyapi
import config

client = freecurrencyapi.Client(config.API_KEY)

LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResponseFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)

    def emit(self, record):
        logging.FileHandler.emit(self, record)


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
    response = requests.get(config.API_URL)
    data = response.json()
    logger.info(f"Response: {data}")
    return data


def get_alternative_exchange_rates():
    response = requests.get(config.ALT_API_URL)
    data = response.json()
    logger.info(f"Response: {data}")
    return data
