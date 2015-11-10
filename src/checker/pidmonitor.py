from . import remoteexec
from . import subprocessmap
from .mylog import log

import shlex

def _check_cmd(searchstring):
    return ["pgrep", "-a", shlex.quote(searchstring)]

def monitor(hosts, process_search):
    cmd = _check_cmd(process_search)
    log.debug("Checking for process %s on hosts %s.", process_search, str(hosts))
    commands = list(map(lambda host: remoteexec.remote_cmd(host, cmd), hosts))
    pidresults = subprocessmap.map(commands)
    log.debug("Got results %s", str(pidresults))
    success = True
    message = "Process {0:s} is running on all hosts".format(process_search)
    for ix, (retcode, stdout, stderr) in enumerate(pidresults):
        if retcode != 0:
            success = False
            message = "Process {0:s} is not running on host {1:s} ({2:d})". \
                      format(process_search, hosts[ix], retcode)
            break
    return {"success": success, "message": message}
