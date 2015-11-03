from .mylog import log
from . import checker
from . import scheduler

import watchdog.events
import watchdog.observers

class UpdateCheckersEvent(watchdog.events.FileSystemEventHandler):
    def on_any_event(self, event):
        log.info("Detected a change in %s. Reloading checkers.",
                 checker.get_checker_config_dir())
        checkers = checker.build_checkers_from_dir()
        scheduler.set_checkers(checkers)

_observer = watchdog.observers.Observer()
        
def start():
    log.info("Loading and setting checkers initially.")
    scheduler.set_checkers(checker.build_checkers_from_dir())
    event_handler = UpdateCheckersEvent()
    _observer.schedule(event_handler, checker.get_checker_config_dir(), recursive=True)
    _observer.schedule(watchdog.events.LoggingEventHandler(), checker.get_checker_config_dir(), recursive=True)
    log.info("Starting filesystem watchdog for %s", checker.get_checker_config_dir())
    _observer.start()

def stop():
    log.info("Stopping filesystem watchdog for %s", checker.get_checker_config_dir())
    _observer.stop()
    _observer.join()
