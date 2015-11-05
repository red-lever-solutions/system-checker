from .mylog import log
from .checkerlog import log_checker_result

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor
import asyncio

_scheduler = AsyncIOScheduler(executors={
    "asyncio": AsyncIOExecutor()
})

_checker_jobs = dict()

def _make_checker_fun(checker):
    def cf():
        log_checker_result(checker[0], checker[2]())
    return cf

def _add_checker(checker):
    log.debug("Adding schedule job for %s", checker[0])
    job = _scheduler.add_job(
        _make_checker_fun(checker),
        IntervalTrigger(seconds=checker[1]),
        id=checker[0],
        name=checker[0],
        replace_existing=True,
        coalesce=True,
        executor="asyncio")
    _checker_jobs[checker[0]] = job

def _remove_checker_jobs():
    global _checker_jobs
    for cid, cjob in _checker_jobs.items():
        cjob.remove()
    _checker_jobs = dict()

def set_checkers(checkers):
    log.debug("Removing all schedule jobs")
    _remove_checker_jobs()
    for checker in checkers:
        _add_checker(checker)

def add_dashboard_updater(updater_fun, interval_seconds):
    log.debug("Adding the dasboard updater job")
    _scheduler.add_job(
        updater_fun,
        IntervalTrigger(seconds=interval_seconds),
        id="Dashboard Updater",
        name="Dashboard Updater",
        replace_existing=True,
        coalesce=True,
        executor="asyncio")

def run():
    log.info("Starting checker scheduler")
    _scheduler.start()
    asyncio.get_event_loop().run_forever()
    log.info("Stopped checker scheduler")
