import logging


def get_custom_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
