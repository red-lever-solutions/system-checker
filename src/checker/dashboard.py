import requests
from operator import itemgetter
import json

from .checkerlog import get_checker_memlog
from .checker import get_checker_config
from .mylog import log
from .scheduler import add_dashboard_updater

TIPBOARD_TILE_NAME = "scrollable_fancy_listing"
TIPBOARD_TILE_ID = "service-checker-tile"
TIPBOARD_API_HOST = "tipboard:8080"
TIPBOARD_API_VERSION = "v0.1"
TIPBOARD_API_KEY = "4c0590d88ff3460d92f4b78714b2c393"
TIPBOARD_UPDATE_INTERVAL = 2

_api_session = requests.Session()

def _base_url():
    return "http://{host:s}/{api_version:s}/{api_key:s}" \
        .format(host=TIPBOARD_HOST,
                api_version=TIPBOARD_API_VERION,
                api_key=TIPBOARD_API_KEY)

def _push_url():
    return "{0:s}/push".format(_base_url())

def _config_url():
    return "{0:s}/tileconfig/{1:s}".format(_base_url(), TIPBOARD_TILE_ID)

def _build_dashboard_data_base(checker_config):
    data = []
    for checker_id, config in checker_config.iteritems():
        clog = get_checker_memlog(checker_id)
        if clog is None:
            continue
        data.append((config.importance,
                     checker_id,
                     config.name,
                     clog.success,
                     clog.message))
    return list(map(lambda t: t[1:], sorted(data, key=itemgetter(0), reverse=True)))

def _build_dashboard_data(data_base):
    return [{
        "label": cr[0],
        "text": cr[1],
        "description": cr[3]
    } for cr in data_base]

def _build_dashboard_config(data_base):
    config = {str(ix): {"label_color": "green" if cr[2] else "red"}
              for ix, cr in enumerate(data_base)}
    config["vertical_center"] = True
    return config

def _push_data(data):
    log.debug("Pushing %s checker results to the dashboard", len(data))
    response = _api_session.post(_push_url(), data={
        "tile": TIPBOARD_TILE_NAME,
        "key": TIPBOARD_TILE_ID,
        "data": json.dumps(data)
    })
    if response.status_code == requests.codes.ok:
        log.debug("Sucessfully pushed checker results")
    else:
        log.warning("Could not push checker results (%s)", response.text)

def _push_config(config):
    log.debug("Pushing %s checker configs to the dashboard", len(config)-1)
    response = _api_session.post(_config_url(), data={
        "value": json.dumps(config)
    })
    if response.status_code == requests.codes.ok:
        log.debug("Sucessfully pushed checker config")
    else:
        log.warning("Could not push checker config (%s)", response.text)

def push():
    data_base = _build_dashboard_data_base(get_checker_config())
    data = _build_dashboard_data(data_base)
    config = _build_dashboard_config(data_base)
    if len(data) > 0:
        _push_data(data)
        _push_config(config)

def init():
    log.info("Activating dashboard updater")
    add_dashboard_updater(push, TIPBOARD_UPDATE_INTERVAL)
