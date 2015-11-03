import socket
from collections import namedtuple
from .mylog import log

EndpointInfo = namedtuple("EndpointInfo", field_names=["host", "port", "timeout"])

def print_endpoint(endpoint):
    return "{0:s}:{1:d}".format(endpoint.host, endpoint.port)


TCPInfo = namedtuple("TCPInfo", field_names=["endpoint", "success", "msg"])

def monitor(endpoint):
    log.debug("Creating a TCP connection for monitoring the endpoint %s",
              print_endpoint(endpoint))
    try:
        sock = socket.create_connection((endpoint.host, endpoint.port), endpoint.timeout)
        log.info("Successfully connected to the endpoint %s",
                 print_endpoint(endpoint))
        return TCPInfo(endpoint=endpoint, success=True, msg="Sucess")
    except Exception as e:
        log.warning("Could not connect to the endpoint %s: %s",
                    print_endpoint(endpoint),
                    str(e))
        return TCPInfo(endpoint=endpoint, success=False, msg=str(e))
    finally:
        try:
            log.debug("Closing the TCP connection")
            sock.close()
        except:
            pass

