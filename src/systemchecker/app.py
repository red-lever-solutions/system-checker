from .mylog import log
from . import tcpmonitor
from . import checkerwatcher
from . import scheduler

def main():
    checkerwatcher.start()
    scheduler.run()
    checkerwatcher.stop()

if __name__ == "__main__":
    main()
