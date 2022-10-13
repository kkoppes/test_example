"""logging and debugging tools"""

import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def get_logger(name, level=logging.DEBUG, log_file=None):
    """get a logger with a file handler and a stream handler"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create file handler which logs even debug messages
    if log_file is None:
        log_file = name + ".log"
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

if __name__ == "__main__":
    logger = get_logger("test_logger")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    logger.info("test_logger.py done")