import pandas as pd

from src.common.constants import SYMBOL, PROFIT_PERCENT, LOSS_PERCENT, INTERVAL, START_TIME
from src.common.item import put_item, get_item
from src.services.binance import client, create_market_order
from src.common.log import logger


def limit_to_buy():
    last24 = client.get_ticker(symbol=SYMBOL)
    high_price = float(last24["highPrice"])
    return high_price


def trade_by_sma():
    bars = client.get_historical_klines(SYMBOL, INTERVAL, START_TIME)
    for line in bars:
        del line[5:]
    df = pd.DataFrame(bars)
    df.columns = ['date', 'open', 'high', 'low', 'close']
    df['5ma'] = df['close'].rolling(25).mean()
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    close = df['close']

    price = float(close.tail(1)[0])
    last_period = close.tail(120)
    max_price_period = float(last_period.max())
    min_price_period = float(last_period.min())
    price_time = close.tail(1).index[0]

    open_order = get_item()
    active_order = int(open_order.get('active', 0))
    open_order_price = float(open_order.get('buy_price', 0))

    stop_loss = open_order_price - (open_order_price * LOSS_PERCENT)
    profit = open_order_price + (open_order_price * PROFIT_PERCENT)
    future_profit = (price * PROFIT_PERCENT) + price

    order_obj = ({
        'time': str(price_time),
        'price': price,
        'max_price': max_price_period,
        'min_price': min_price_period,
        'profit': profit,
        'future_profit': future_profit,
        'order_price': open_order_price,
        'stop_loss': stop_loss
    })

    if future_profit < max_price_period > price and active_order == 0:
        put_item(1, price)
        create_market_order('BUY')
        logger.info('>BUY {}'.format(price))
        print(order_obj)

    if min_price_period < price > profit and active_order == 1:
        logger.info('>SELL {}'.format(price))
        print(order_obj)
        create_market_order('SELL')
        put_item(0, 0)

    if stop_loss > price and active_order == 1:
        logger.info('>SELL LOSS {}'.format(price))
        create_market_order('SELL')
        put_item(0, 0)

    return True
