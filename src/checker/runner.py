from .mylog import log
from . import tcpmonitor
from . import checkerwatcher
from . import scheduler
from . import dashboard

def main():
    checkerwatcher.start()
    dashboard.init()
    scheduler.run()
    checkerwatcher.stop()

if __name__ == "__main__":
    main()
