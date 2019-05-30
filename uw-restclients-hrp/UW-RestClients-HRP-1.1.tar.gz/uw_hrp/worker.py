"""
This is the interface for interacting with the HRP Web Service.
"""

from datetime import datetime
import logging
import json
from restclients_core.exceptions import InvalidRegID, InvalidNetID,\
    InvalidEmployeeID
from uw_pws import PWS
from uw_hrp import get_resource
from uw_hrp.models import Worker


logger = logging.getLogger(__name__)
URL_PREFIX = "/hrp/v2/worker"


def get_worker_by_employee_id(employee_id):
    if not PWS().valid_employee_id(employee_id):
        raise InvalidEmployeeID(employee_id)
    return _get_worker(employee_id)


def get_worker_by_netid(netid):
    if not PWS().valid_uwnetid(netid):
        raise InvalidNetID(netid)
    return _get_worker(netid)


def get_worker_by_regid(regid):
    if not PWS().valid_uwregid(regid):
        raise InvalidRegID(regid)
    return _get_worker(regid)


def _get_worker(id):
    """
    Return a restclients.models.hrp.WorkerPerson object
    """
    url = "{0}/{1}.json".format(URL_PREFIX, id)
    return Worker(data=json.loads(get_resource(url)))
