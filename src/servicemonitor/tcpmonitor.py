import socket
import namedtuple
from mylog import log

EndpointInfo = namedtuple(["host", "port", "timeout"])

def print_endpoint(endpoint):
    return "{0}:{1:s}".format(endpoint.host, endpoint.port)


TCPInfo = namedtuple(["endpoint", "success", "msg"])

def monitor(endpoint):
    log.debug("Creating a TCP connection for monitoring the endpoint %s",
              print_endpoint(endpoint))
    try:
        sock = socket.create_connection((endpoint.host, endpoint.port), endpoint.timeout)
        sock.recv(4096)
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
            sock.close()
