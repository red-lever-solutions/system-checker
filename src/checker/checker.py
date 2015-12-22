from . import tcpmonitor
from . import awsmonitor
from . import pidmonitor
from . import dnsmonitor
from . import filesyncmonitor
from . import httpstatusmonitor
from . import hostping
from .mylog import log

import os
from glob import glob
import yaml
from collections import namedtuple

CheckerConfig = namedtuple("CheckerConfig", field_names=[
    "interval_seconds",
    "importance",
    "name",
    "config"
])

CheckerResult = namedtuple("CheckerResult", field_names=[
    "success",
    "message"
])

CHECKER_CONFIG_DIR = "/config/checkers"

def get_checker_config_dir():
    return CHECKER_CONFIG_DIR

def build_checker(checker_name, checker_config):
    checker_builder = _checker_builder_map.get(checker_name)
    if checker_builder is None:
        raise RuntimeError("Could not find checker with name %s.", checker_name)
    return checker_builder(**checker_config)

def _build_tcpmonitor(host, port, timeout):
    def cf():
        res = tcpmonitor.monitor(tcpmonitor.EndpointInfo(
            host=host,
            port=port,
            timeout=timeout))
        return CheckerResult(success=res.success, message=res.message)
    return cf

def _build_hostping(host, timeout):
    def cf():
        res = hostping.monitor(hostping.PingTarget(
            host=host,
            timeout=timeout))
        return CheckerResult(success=res.success, message=res.message)
    return cf

def _build_awsmonitor(services):
    def cf():
        res = awsmonitor.monitor(services)
        return CheckerResult(success=res.success, message=res.message)
    return cf

def _build_pidmonitor(hosts, process_search):
    def cf():
        res = pidmonitor.monitor(hosts, process_search)
        return CheckerResult(success=res["success"], message=res["message"])
    return cf

def _build_dnsmonitor(dns_names):
    def cf():
        res = dnsmonitor.monitor(dns_names)
        return CheckerResult(success=res["success"], message=res["message"])
    return cf

def _build_filesyncmonitor(hosts, file_path):
    def cf():
        res = filesyncmonitor.monitor(hosts, file_path)
        return CheckerResult(success=res["success"], message=res["message"])
    return cf

def _build_httpstatusmonitor(url, method="GET", data=None, headers=None, verify_ssl=True):
    def cf():
        res = httpstatusmonitor.monitor(url, method, data, headers, verify_ssl)
        return CheckerResult(success=res["success"], message=res["message"])
    return cf

_checker_builder_map = {
    "TCPListen": _build_tcpmonitor,
    "AWSStatus": _build_awsmonitor,
    "ProcessMonitor": _build_pidmonitor,
    "FileSync": _build_filesyncmonitor,
    "HostPing": _build_hostping,
    "HTTPStatus": _build_httpstatusmonitor,
    "DNS": _build_dnsmonitor
}

def _checker_id_from_filename(filename):
    return os.path.splitext(filename)[0]

_checker_configs = dict()

def build_checker_from_file(filename):
    with open(os.path.join(get_checker_config_dir(), filename), 'r') as f:
        try:
            checker_config = CheckerConfig(**yaml.load(f))
        except:
            raise RuntimeError("Incomplete checker configuration in file %s", filename)
        checker_id = _checker_id_from_filename(filename)
        _checker_configs[checker_id] = checker_config
        return (checker_id,
                checker_config.interval_seconds,
                build_checker(checker_config.name, checker_config.config))

def build_checkers_from_dir():
    globres = glob(os.path.join(get_checker_config_dir(), "[!_]*.yaml"))
    checker_filenames = [os.path.basename(f) for f in globres]
    _checker_configs = dict()
    checkers = []
    for filename in checker_filenames:
        try:
            checkers.append(build_checker_from_file(filename))
        except Exception as e:
            log.exception("Failed to load checker from %s", filename)
    return checkers

def get_checker_config(checker_id):
    if not checker_id in _checker_configs:
        log.error("Checker %s not found.", checker_id)
    return _checker_configs.get(checker_id)

def get_checker_config_dict():
    return _checker_configs
