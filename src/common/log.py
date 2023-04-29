import os
from logging import getLogger, config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            'format': '%(levelname)s %(message)s'
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "api-logger": {
            "handlers": ["default"],
            "level": os.environ.get("LOG_LEVEL", "DEBUG")
        },
    },
}

config.dictConfig(log_config)

logger = getLogger('api-logger')


# import logging
# from logging.config import dictConfig
#
# logging_config = dict(
#     version = 1,
#     formatters = {
#         'f': {'format':
#               '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
#         },
#     handlers = {
#         'h': {'class': 'logging.StreamHandler',
#               'formatter': 'f',
#               'level': logging.DEBUG}
#         },
#     root = {
#         'handlers': ['h'],
#         'level': logging.DEBUG,
#         },
# )
#
# dictConfig(logging_config)
#
# logger = logging.getLogger()
