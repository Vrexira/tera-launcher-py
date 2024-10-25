import logging


def std_out(message, code = None):
    if code is None:
        code = 9000
    logging.info(f"{code}: {message}")
