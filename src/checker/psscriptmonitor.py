from . import remoteexec
from . import subprocessmap
from .mylog import log

import shlex

def _check_cmd(script):
    return ["powershell", shlex.quote(script)]

def monitor(hosts, script):
    cmd = _check_cmd(script)
    log.debug("Running script %s on hosts %s.", script, str(hosts))
    commands = list(map(lambda host: remoteexec.remote_cmd(host, cmd, ssh_config="ssh_config_win"), hosts))
    pidresults = subprocessmap.map(commands)
    log.debug("Got results %s", str(pidresults))
    success = True
    message = "Successful on all hosts"
    for ix, (retcode, stdout, stderr) in enumerate(pidresults):
        if retcode != 0:
            success = False
            message = "Error on host {0:s}({1:d}): {2:s}" \
                      .format(hosts[ix], retcode, stdout.decode('ascii')+stderr.decode('ascii'))
            break
    return {"success": success, "message": message}
