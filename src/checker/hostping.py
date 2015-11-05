import subprocess
from collections import namedtuple
from .mylog import log

PingTarget = namedtuple("PingTarget", field_names=["host", "timeout"])

PingInfo = namedtuple("PingInfo", field_names=["target", "success", "message"])

def monitor(target):
    log.debug("Pinging host %s", target.host)
    status, response = subprocess.getstatusoutput(
        "ping -c1 -w{0:d} {1:s}".format(target.timeout, target.host))
    log.debug("Got ping response: %s", response)
    if status == 0:
        response = response.split("\n")[1]
        return PingInfo(target=target, success=True, message=response)
    else:
        return PingInfo(target=target,
                        success=False,
                        message="Ping {0:s}: Error ({1:d})".format(target.host, status))
