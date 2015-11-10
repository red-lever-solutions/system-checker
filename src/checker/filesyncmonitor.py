from . import remoteexec
from . import subprocessmap
from .mylog import log

import shlex
from operator import itemgetter
from itertools import dropwhile

def _filehash_cmd(filepath):
    return ["md5sum {0:s} | cut -d' ' -f1".format(shlex.quote(filepath))]

def monitor(hosts, filepath):
    cmd = _filehash_cmd(filepath)
    log.debug("Checking hash of file %s on hosts %s.", filepath, str(hosts))
    commands = list(map(lambda host: remoteexec.remote_cmd(host, cmd), hosts))
    hashresults = subprocessmap.map(commands)
    log.debug("Got results %s", str(hashresults))
    statuscodes = map(itemgetter(0), hashresults)
    success = all(map(lambda c: c==0, statuscodes))
    if success is True:
        hashes = list(map(itemgetter(1), hashresults))
        all_same = len(set(hashes)) <= 1
        if all_same:
            message = "File {0:s} is identical on all hosts".format(filepath)
            mon_success = True
        else:
            message = "File {0:s} is not in sync".format(filepath)
            mon_success = False
        return {"success": mon_success, "message": message}
    else:
        errmsg = list(dropwhile(lambda res: res[0] == 0, hashresults))[0][2].decode("ascii")
        return {"success": False, "message": errmsg}
