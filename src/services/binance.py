from binance.client import Client

from src.common.constants import BTC_QTD, SYMBOL


api_key = 'hNCkQJauH4nLLpTDxrxqlAMDXzQf3CwR90x1kNonwZtwgCaua8YP8LWB47dpzwJk'
api_secret = '3ZUa7lBCUKXYPTTyVMI8FYECiPVbmjmC2wpaEsuIzRO0jx5OrjUu4ETSenDW9xV5'

client = Client(api_key=api_key, api_secret=api_secret, tld='com')


def create_order(price, order_type='BUY', quantity=BTC_QTD):
    client.create_order(symbol=SYMBOL, side=order_type, type="LIMIT", quantity=quantity,
                        price=price, timeInForce="GTC")
    print('EXECUTED ORDER TYPE:{}, PRICE: {}'.format(order_type, price))


def create_market_order(order_type='BUY', quantity=BTC_QTD):
    client.create_order(symbol=SYMBOL, side=order_type, type="MARKET", quantity=quantity)
    print('EXECUTED ORDER: {} QTD: {}'.format(order_type, quantity))

