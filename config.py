import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

BASIC_USD = 34.0
BASIC_USDT = 33.9
BASIC_RUB = 2.4

BOT_LINK = 'https://t.me/XChange_money_bot'

# headers for requests
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

# binance url for requests
URL_BINANCE = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

# minimal orders count for binance p2p
ORDERS = 10

# minimal orders rate for binance p2p
ORDERS_RATE = 0.95

# banks for binance p2p
BANKS = ['TinkoffNew']

# coin for binance p2p
COIN = 'USDT'

# types of delivery and their coeff
TYPE_COEFF ={
    'delivery' : 1.025,
    'kata' : 1.025,
    'ravai' : 1.025,
    'airport' : 1.025,
    'atm' : 1.022,
    'office' : 1.021,
    'transfer' : 1.02,
    'service' : 1.02,
}

# types of delivery and their minimal amount
TYPE_AMOUNT ={
    'delivery' : 40000,
    'kata' : 20000,
    'ravai' : 10000,
    'airport' : 40000,
    'atm' : 10000,
    'office' : 5000,
    'transfer' : 5000,
    'service' : 5000,
}