import time

from src.common.log import logger

from src.handlers.trade import trade_by_sma
from src.handlers.trade_high_low import trade_high_low
if __name__ == '__main__':
    logger.info('app.start')
    while True:
        trade_by_sma()
        trade_high_low()
        time.sleep(60)
