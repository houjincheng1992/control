#coding=utf-8
import os
import logging


class SingletonMeta(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.instance

    def __new__(mcs, name, bases, dct):
        return type.__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(SingletonMeta, cls).__init__(name, bases, dct)


LOGGING_DIR = os.path.dirname(os.path.dirname(__file__))
LOGGING_DIR = os.path.dirname(LOGGING_DIR)
LOGGING_DIR = os.path.join(LOGGING_DIR, "logs")

if not os.path.isdir(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)


class Logger(object):
    """
    日志对象的工厂类，保证单例
    """

    __metaclass__ = SingletonMeta

    logger_dict = {}

    def __init__(self, level="DEBUG"):
        self.level = level

    def get_logger(self, module):
        if module in self.logger_dict:
            return self.logger_dict[module]
        logger = self.create_logger(module)
        self.logger_dict[module] = logger
        return logger

    def create_logger(self, module):
        logger = logging.getLogger(module)
        default_logger_level = getattr(logging, os.getenv("LOG_LEVEL", self.level))

        logger.setLevel(default_logger_level)

        # setup console logger handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(default_logger_level)

        formatter = logging.Formatter('%(asctime)s [RequestID:%(thread)d] '
                                      '[%(name)s:%(lineno)d] '
                                      '[%(module)s:%(funcName)s] '
                                      '[%(levelname)s]- %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        return logger

    def set_level(self, level):
        self.level = level


def getLogger(module, level="DEBUG"):
    # Disable the default logging config
    # LOGGING_CONFIG = None

    log = Logger()
    log.set_level(level)

    logger = log.get_logger(module)

    return logger
