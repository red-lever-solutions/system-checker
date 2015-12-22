from .mylog import log

import requests

def monitor(url, method="GET", data=None, headers=None, verify_ssl=True):
    log.debug("Checking http status code of %s", url)
    try:
        if method.lower() == "get":
            response = requests.get(url, data=data, headers=headers, verify=verify_ssl)
        elif method.lower() == "post":
            response = requests.post(url, data=data, headers=headers, verify=verify_ssl)
        else:
            raise Exception("Method not supported {:s}".format(method.upper()))
    except Exception as e:
        return {"success": False, "message": str(e)}
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
