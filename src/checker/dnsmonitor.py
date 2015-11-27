from collections import namedtuple
import socket
from .mylog import log

def check_dns_name(dns_name, ip):
    resolvip = socket.gethostbyname(dns_name)
    return (resolvip == ip, resolvip)

def monitor(dns_names):
    for dns_name, ip in dns_names.items():
        log.info("Checking DNS name {0:s}. Should be {1:s}".format(dns_name, ip))
        success, resolvip = check_dns_name(dns_name, ip)
        if not success:
            return {
                "success": False,
                "message": "DNS name {0:s} resolves to {1:s}. Expected {2:s}"\
                .format(dns_name, resolvip, ip)
            }
    return {
        "success": True,
        "message": "DNS names resolve correctly"
    }
