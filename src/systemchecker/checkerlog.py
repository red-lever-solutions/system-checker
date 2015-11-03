import logging
from logging.handlers import TimedRotatingFileHandler
import os
import ujson
from collections import OrderedDict
from datetime import datetime

CHECKER_LOG_DIR = "/status"

def get_checker_log_dir():
    return CHECKER_LOG_DIR

_checker_loggers = dict()

def get_checker_logger(checker_id):
    if checker_id in _checker_loggers:
        return _checker_loggers[checker_id]
    checker_logger = logging.getLogger(checker_id)
    checker_logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(
        filename=os.path.join(get_checker_log_dir(),
                              "{0:s}.log".format(checker_id)),
        when="midnight",
        backupCount=10,
        utc=True)
    handler.setFormatter(logging.Formatter("%(message)s"))
    checker_logger.addHandler(handler)
    _checker_loggers[checker_id] = checker_logger
    return checker_logger

def log_checker_result(checker_id, checker_result):
    logger = get_checker_logger(checker_id)
    logger.info(ujson.dumps(OrderedDict([
        ("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
        ("checker_id", checker_id),
        ("result", vars(checker_result))
    ])))
