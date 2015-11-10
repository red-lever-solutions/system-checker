from .mylog import log

import requests

def monitor(url):
    log.debug("Checking http status code of %s", url)
    response = requests.get(url)
    log.debug("Got status code %s", response.status_code)
    if response.status_code == requests.codes.ok:
        success = True
        message = "{0:s} ({1:d})".format(url, response.status_code)
    else:
        success = False
        message = "{0:s} ({1:d})".format(url, response.status_code)
    return {
        "success": success,
        "message": message
    }
