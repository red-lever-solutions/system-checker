import logging
from logging.handlers import TimedRotatingFileHandler
import os
import json
from collections import OrderedDict
from datetime import datetime

CHECKER_LOG_DIR = "/logs"
CHECKER_STATUS_DIR = "/status"

def get_checker_log_dir():
    return CHECKER_LOG_DIR

def get_checker_status_dir():
    return CHECKER_STATUS_DIR

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

def get_checker_writer(checker_id):
    return open(os.path.join(get_checker_status_dir(),
                             "{0:s}.json".format(checker_id)),
                "w")

def _checker_result_record(checker_id, checker_result):
    return OrderedDict([
        ("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
        ("checker_id", checker_id),
        ("result", vars(checker_result))
    ])

def write_checker_log(checker_id, checker_result):
    logger = get_checker_logger(checker_id)
    logger.info(json.dumps(_checker_result_record(checker_id, checker_result)))

def write_checker_status(checker_id, checker_result):
    with get_checker_writer(checker_id) as w:
        w.write(json.dumps(
            _checker_result_record(checker_id, checker_result),
            indent=2
        ))
        w.write('\n')
        w.flush()
        os.fsync(w.fileno())

def log_checker_result(checker_id, checker_result):
    write_checker_status(checker_id, checker_result)
    write_checker_log(checker_id, checker_result)
