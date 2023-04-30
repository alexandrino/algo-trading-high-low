import time

from src.common.log import logger

from src.handlers.trade import trade_by_sma
if __name__ == '__main__':
    logger.info('app.start')
    while True:
        trade_by_sma()
        time.sleep(60)
