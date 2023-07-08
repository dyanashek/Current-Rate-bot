import requests
import time
import datetime

import config
import rates

def p2p_binance(currency = 'THB', amount = ''):
    """Gets price of buying or selling usdt on Binance p2p."""

    # indicate trade side
    side = 'BUY'
    if currency == 'THB':
        side = 'SELL'
    
    pay_types = []
    if currency == 'RUB':
        pay_types = config.BANKS

    # construct params
    data_binance = {
        "asset": config.COIN,
        "countries": [],
        "fiat": currency,
        "page": 1,
        "proMerchantAds": False,
        "publisherType": None,
        "rows": 20,
        "tradeType": side,
        "transAmount": amount,
        "payTypes" : pay_types,
    }

    # make a request
    try:
        deals = requests.post(url=config.URL_BINANCE, json=data_binance, headers=config.HEADERS).json().get('data')
    except:
        deals = None
    
    if deals is not None:

        for deal in deals:
            # extract merchants order count and rate
            order_count = int(deal.get('advertiser').get('monthOrderCount'))
            finish_rate = float(deal.get('advertiser').get('monthFinishRate'))

            # extract price if the merchant fits params
            if order_count >= config.ORDERS and finish_rate >= config.ORDERS_RATE:
                price = float(deal.get('adv').get('price'))

                return price


def get_exchange_rate(currency, delivery_type, amount_currency='THB', amount=''):
    """Calculates exchange rates depends on amounts and type of delivery."""

    if amount == '':
        amount = config.TYPE_AMOUNT[delivery_type]
    
    coeff = config.TYPE_COEFF[delivery_type]

    if amount_currency == 'THB':
        thb_price = p2p_binance(amount=amount)

        if currency == 'RUB':
            rub_amount = round(amount * config.BASIC_RUB, 2)
            rub_price = p2p_binance(currency='RUB', amount=rub_amount)

            rate = round(rub_price / thb_price * coeff, 3) 
        
        elif currency == 'USD':
            usd_amount = round(amount / config.BASIC_USD, 2)
            usd_price = p2p_binance(currency='USD', amount=usd_amount)

            rate = round(thb_price / usd_price / coeff, 3) 
        
        elif currency == 'USDT':
            rate = round(thb_price / coeff, 3) 
    
    else:
        if currency == 'RUB':
            rub_price = p2p_binance(currency='RUB', amount=amount)
            thb_amount = round(amount / config.BASIC_RUB, 2)
            thb_price = p2p_binance(amount=thb_amount)

            rate = round(rub_price / thb_price * coeff, 3) 
        
        elif currency == 'USD':
            usd_price = p2p_binance(currency='USD', amount=amount)
            thb_amount = round(amount * config.BASIC_USD, 2)
            thb_price = p2p_binance(amount=thb_amount)

            rate = round(thb_price / usd_price / coeff, 3) 

        elif currency == 'USDT':
            thb_amount = round(amount * config.BASIC_USDT, 2)
            thb_price = p2p_binance(amount=thb_amount)

            rate = round(thb_price / coeff, 3) 

    return rate


def get_basic_exchange_rate(currency):
    """Gets minimal rate for currency pair."""

    thb_price = p2p_binance()

    if currency == 'RUB':
        rub_price = p2p_binance(currency)
        rate = round(rub_price / thb_price, 3)

    elif currency == 'USD':
        usd_price = p2p_binance(currency)
        rate = round(thb_price / usd_price, 3)
    
    elif currency == 'USDT':
        rate = round(thb_price, 3)

    return rate


def set_basic_exchange_rate():
    """Sets basic rates in a loop."""

    while True:
        try:
            config.BASIC_USD = get_basic_exchange_rate('USD')
            config.BASIC_USDT = get_basic_exchange_rate('USDT')
            config.BASIC_RUB = get_basic_exchange_rate('RUB')
        except:
            pass

        time.sleep(15)


def set_specific_exchange_rate():
    while True:
        try:
            rates.RUB_DELIVERY_RATE = get_exchange_rate('RUB', 'delivery')
            rates.RUB_AIRPORT_RATE = get_exchange_rate('RUB', 'airport')
            rates.RUB_ATM_RATE = get_exchange_rate('RUB', 'atm')
            rates.RUB_OFFICE_RATE = get_exchange_rate('RUB', 'office')
            rates.RUB_TRANSFER_RATE = get_exchange_rate('RUB', 'transfer')
            rates.RUB_SERVICE_RATE = get_exchange_rate('RUB', 'service')
            
            rates.USDT_DELIVERY_RATE = get_exchange_rate('USDT', 'delivery')
            rates.USDT_AIRPORT_RATE = get_exchange_rate('USDT', 'airport')
            rates.USDT_ATM_RATE = get_exchange_rate('USDT', 'atm')
            rates.USDT_OFFICE_RATE = get_exchange_rate('USDT', 'office')
            rates.USDT_TRANSFER_RATE = get_exchange_rate('USDT', 'transfer')
            rates.USDT_SERVICE_RATE = get_exchange_rate('USDT', 'service')

            rates.USD_DELIVERY_RATE = get_exchange_rate('USD', 'delivery')
            rates.USD_AIRPORT_RATE = get_exchange_rate('USD', 'airport')
            rates.USD_ATM_RATE = get_exchange_rate('USD', 'atm')
            rates.USD_OFFICE_RATE = get_exchange_rate('USD', 'office')
            rates.USD_TRANSFER_RATE = get_exchange_rate('USD', 'transfer')
            rates.USD_SERVICE_RATE = get_exchange_rate('USD', 'service')
        except:
            pass

        time.sleep(60)


def currency_rate_message():
    """Generates a message with currency rates and terms of use."""

    current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%d.%m.%Y %H:%M")

    text = f'''
        \n*Курс на {current_time}* 🗓\
        \n\
        \n💱 *THB/RUB*:\
        \nКурьерская доставка - *{rates.RUB_DELIVERY_RATE}*\
        \nДоставка в аэропорт - *{rates.RUB_AIRPORT_RATE}*\
        \nВыдача через банкомат - *{rates.RUB_ATM_RATE}*\
        \nПеревод на тайский счет - *{rates.RUB_TRANSFER_RATE}*\
        \nОплата услуг - *{rates.RUB_TRANSFER_RATE}*\
        \n\
        \n💰 *USDT/THB*:\
        \nКурьерская доставка - *{rates.USDT_DELIVERY_RATE}*\
        \nДоставка в аэропорт - *{rates.USDT_AIRPORT_RATE}*\
        \nВыдача через банкомат - *{rates.USDT_ATM_RATE}*\
        \nПеревод на тайский счет - *{rates.USDT_TRANSFER_RATE}*\
        \nОплата услуг - *{rates.USDT_TRANSFER_RATE}*\
        \n\
        \n*Минимальная сумма выдачи*:\
        \nКурьерская доставка от *40 000 THB*:\
        \n- для *района Ката* от *20 000 THB*\
        \n- для *районов Равай и Найхарн* от *10 000 THB*\
        \n\
        \nВ аэропорт от *40 000 THB*\
        \nЧерез банкомат от *10 000 THB*\
        \nНа тайский счет от *5 000 THB*\
        \nОплата услуг от *5 000 THB*\
        \n\
        \n❗️*ВАЖНО*❗️\
        \nВ сообщении представлены справочные данные. Курс меняется в режиме реального времени и может отличаться в зависимости от суммы обмена. Для более точного расчета воспользуйтесь *калькулятором обмена*.\
    '''

    #     text = f'''
    #         \n*Course to {current_date}* 🗓\
    #         \n\
    #         \n💱 *THB/RUB*:\
    #         \nCourier delivery - *{rates.RUB_DELIVERY_RATE}*\
    #         \nAirport delivery - *{rates.RUB_AIRPORT_RATE}*\
    #         \nWithdrawal via ATM - *{rates.RUB_ATM_RATE}*\
    #         \nTransfer to Thai account - *{rates.RUB_TRANSFER_RATE}*\
    #         \nPayment for services - *{rates.RUB_TRANSFER_RATE}*\
    #         \n\
    #         \n💰 *USDT/THB*:\
    #         \nCourier delivery - *{rates.USDT_DELIVERY_RATE}*\
    #         \nAirport Delivery - *{rates.USDT_AIRPORT_RATE}*\
    #         \nATM withdrawal - *{rates.USDT_ATM_RATE}*\
    #         \nTransfer to Thai account - *{rates.USDT_TRANSFER_RATE}*\
    #         \nPayment for services - *{rates.USDT_TRANSFER_RATE}*\
    #         \n\
    #         \n*Minimum withdrawal amount*:\
    #         \nCourier delivery from *40 000 THB*:\
    #         \n- for *Kata area* from *20 000 THB*\
    #         \n- for *Rawai and Naiharn districts* from *10,000 THB*\
    #         \n\
    #         \nTo the airport from *40 000 THB*\
    #         \nVia ATM from *10 000 THB*\
    #         \nTo Thai account from *5 000 THB*\
    #         \nPayment for services from *5 000 THB*\
    #         \n\
    #         \n❗️*IMPORTANT*❗️\
    #         \nThe message contains reference data. The rate changes in real time and may differ depending on the amount of the exchange. For a more accurate calculation, use the *exchange calculator*.\
    #     '''

    return text