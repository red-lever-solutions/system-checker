from .mylog import log
from . import tcpmonitor

def main():
    mres = tcpmonitor.monitor(tcpmonitor.EndpointInfo(
        host="alphary-lb1.alphary-english.net",
        port=80,
        timeout=10
    ))
    log.info("Got monitoring result: %s", mres)

if __name__ == "__main__":
    main()
