from bs4 import BeautifulSoup
import requests
from collections import namedtuple
import re

from .mylog import log

_session = requests.Session()

AWSInfo = namedtuple("AWSInfo", field_names=["success", "message"])

def _request_status_page():
    response = _session.get("http://status.aws.amazon.com")
    if response.status_code != requests.codes.ok:
        return None
    else:
        return response.text

def _parse_status_page(page, services):
    soup = BeautifulSoup(page, 'lxml')
    events_soup = soup.find(id="current_events_block")
    service_regexes = map(lambda s: re.compile(re.escape(s)), services)
    tds = events_soup.find_all("td", string=services)
    messages = list(map(lambda td: td.find_next_sibling("td").string.strip(), tds))
    log.debug("Parsed AWS status messages: %s", str(messages))
    return messages

_ok_message_re = re.compile("Service is operating normally")

def _validate_status_messages(services, messages):
    success = True
    message = "AWS is awesome!"
    for ix, msg in enumerate(messages):
        if _ok_message_re.search(msg) is None:
            success = False
            message = "{0:s}: {1:s}".format(services[ix], msg)
            break
    return AWSInfo(success=success, message=message)
        
def monitor(services):
    return _validate_status_messages(
        services,
        _parse_status_page(_request_status_page(), services))
