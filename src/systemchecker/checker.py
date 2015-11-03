from . import tcpmonitor
from .mylog import log

import os
from glob import glob
import yaml

CHECKER_CONFIG_DIR = "/config"

def get_checker_config_dir():
    return CHECKER_CONFIG_DIR

def build_checker(checker_name, checker_config):
    checker_builder = _checker_builder_map.get(checker_name)
    if checker_builder is None:
        raise RuntimeError("Could not find checker with name %s.", checker_name)
    return checker_builder(**checker_config)

def _build_tcpmonitor(host, port, timeout):
    return lambda: tcpmonitor.monitor(tcpmonitor.EndpointInfo(
        host=host,
        port=port,
        timeout=timeout))

_checker_builder_map = {
    "TCPListen": _build_tcpmonitor
}

def _checker_id_from_filename(filename):
    return os.path.splitext(filename)[0]

def build_checker_from_file(filename):
    with open(os.path.join(get_checker_config_dir(), filename), 'r') as f:
        checker_config = yaml.load(f)
        if not (frozenset(["interval_seconds", "name", "config"]) <= \
                frozenset(checker_config.keys())):
            raise RuntimeError("Incomplete checker configuration in file %s", filename)
        return (_checker_id_from_filename(filename),
                checker_config["interval_seconds"],
                build_checker(checker_config["name"], checker_config["config"]))

def build_checkers_from_dir():
    globres = glob(os.path.join(get_checker_config_dir(), "[!_]*.yaml"))
    checker_filenames = [os.path.basename(f) for f in globres]
    checkers = []
    for filename in checker_filenames:
        try:
            checkers.append(build_checker_from_file(filename))
        except Exception as e:
            log.exception("Failed to load checker from %s", filename)
    return checkers
