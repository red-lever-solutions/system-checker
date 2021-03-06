import logging
import time

logging.basicConfig(
    level = logging.WARNING,
    format = '%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)
logging.Formatter.converter = time.gmtime

log = logging
