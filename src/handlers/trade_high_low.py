import pandas as pd

from src.common.constants import SYMBOL, BTC_QTD, PROFIT_PERCENT, LOSS_PERCENT, INTERVAL, START_TIME
from src.common.item import put_item, get_item
from src.services.binance import client, create_market_order, create_order
from src.common.log import logger


def limit_to_buy():
    last24 = client.get_ticker(symbol=SYMBOL)
    high_price = float(last24["highPrice"])
    return high_price


def trade_high_low():
    bars = client.get_historical_klines(SYMBOL, INTERVAL, START_TIME)
    for line in bars:
        del line[5:]
    df = pd.DataFrame(bars)
    df.columns = ['date', 'open', 'high', 'low', 'close']
    df['5ma'] = df['close'].rolling(7).mean()
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df['close'] = df.close.astype(float)
    close = df['close']
    price = float(close.tail(1)[0])
    price_time = close.tail(1).index[0]
    sma25_price = float(close.rolling(25).mean().tail(1)[0])
    sma25_price = sma25_price
    sma = close.rolling(25).mean()
    sma = float(sma.tail(25).mean())

    open_order = get_item()
    open_order_price = float(open_order.get('buy_price', 0))

    active_order = int(open_order.get('active', 0))
    buy_price_with_profit = (open_order_price * PROFIT_PERCENT) + open_order_price
    future_profit = (price * PROFIT_PERCENT) + price
    stop_loss = open_order_price - (open_order_price * LOSS_PERCENT)

    high_price_24h = limit_to_buy()
    max_price_period = float(close.tail(120).max())

    log_obj = {
        'time': str(price_time),
        'price': price,
        'sma25_price': sma25_price,
        'sma': sma,
        'max_price': max_price_period,
        'profit': buy_price_with_profit,
        'future_profit': future_profit,
        'order_price': open_order_price,
        'stop_loss': stop_loss
    }

    if sma25_price > sma and price < max_price_period > future_profit and active_order == 0:
        create_order(price, 'BUY', BTC_QTD)
        logger.info(log_obj)
        logger.info('>BUY: {}'.format(price))
        put_item(1, price)

    if price >= buy_price_with_profit and active_order == 1:
        create_order(price, 'SELL', BTC_QTD)
        logger.info(log_obj)
        logger.info('>SELL1: {}'.format(price))

        put_item(0, price)

    # sell with profit
    elif active_order == 1 and sma25_price < sma and buy_price_with_profit < price:
        create_order(price, 'SELL', BTC_QTD)
        logger.info(log_obj)
        logger.info('>SELL2: {}'.format(price))
        put_item(0, price)

    # STOP LOSS
    elif active_order == 1 and price < stop_loss:
        create_market_order('SELL', BTC_QTD)
        logger.info(log_obj)
        logger.info('STOP LOSS SELL: {}'.format(price))

        put_item(0, price)

    logger.info(log_obj)

    return True
