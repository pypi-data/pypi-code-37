from time import time, sleep
from random import randint
from datetime import datetime
from json import loads, dumps
import weakref
import pandas as pd
import msgpack
import socket
import pickle
from locust import runners, events, stats, web
# from abc import ABC, abstractmethod


from .display import DEBUG, WARN, SCALER
from .exceptions import *
from .insight import Insight



# class Subject(ABC):
#     """
#     The Subject interface declares common operations for both LocustEndpoint and
#     the Proxy
#     """

#     @abstractmethod
#     def request(self):
#         pass



# class Rule(Subject):
#     """
#     The Proxy has an interface identical to the RealSubject.
#     """

#     def __init__(self, real_subject):
#         self._real_subject = real_subject

#     def request(self):
#         if self.resolve():
#             self._real_subject.request()


#     def resolve(self):
        
#         return True


class LocustEndpoint():

    instances   = list()
    previous    = None

    def __init__(self, endpoint, methods, name=None, headers=None,
                    body=None, get_body_type=None, post_body_type='json',
                    redirects=True):
        """Core backpack class representing endpoints and their data"""

        self.__class__.instances.append(self)
        self.__nonzero__ = self.__bool__    # For Python 2 compatibility

        self.endpoint   = endpoint
        self.name       = name if name is not None else endpoint
        self.original   = self.name
        self.original_e = self.endpoint
        self.methods    = methods
        self.headers    = headers if headers is not None else {}
        self.body       = body if body is not None else {}
        self.get_body_type = get_body_type
        self.post_body_type = post_body_type
        self.redirects  = redirects
        self.instance   = None
        self.Result     = None

        self.columns    = ['response_time', 'status']
        self.statistics = pd.DataFrame(columns=self.columns)

        self.current_pivot = False
        self.sealed = False
        self.debug = False



    def __add__(self, member):
        """LocustEndpoint addition support for chaining dependant requests"""

        if not self.current_pivot:
            self.Request()
            self.current_pivot = True
        if self.Result.success: 
            member.Request()
            member.current_pivot = True
        self.current_pivot   = False
        return member


    def __bool__(self):
        """Bool implementation for easier result checking
            Example: if <LocustEndpoint>: 
                returns True if <LocustEndpoint>.Result.success is True"""

        try:
            if self.Result.success: return True
            else: return False
        except: return False

    # def __call__(self, rule):
    #     pass


    @property
    def seal(self):
        """Blocks this LocustEndpoint from doing requests until unsealed"""
        self.sealed = True
        self.Result = self.RequestResult(False, 'null', self.endpoint)
        WARN("{} SEALED".format(self.endpoint))

    @property
    def unseal(self):
        """Unseals the sealed LocustEndpoint to re-enable requests"""
        self.sealed = False
        WARN("{} UNSEALED".format(self.endpoint))


    def attach(self, caller): self.instance = caller

    @property
    def DEBUG_MODE_ON(self):
        self.debug = True
        DEBUG("DEBUG MODE ACTIVATED FOR {}".format(self.endpoint))

    @property
    def DEBUG_MODE_OFF(self):
        self.debug = False
        DEBUG("DEBUG MODE DEACTIVATED FOR {}".format(self.endpoint))

    def bank_statistics(self, response_time, status):
        prev = self.previous.endpoint if self.previous is not None else 'First'
        data = {
            'response_time' : response_time,
            'status'        : status,
            'previous_req'  : prev,
            'stamp'         : datetime.now().strftime('%H:%M:%S')
        }
        self.statistics = self.statistics.append(data, ignore_index=True)


    def Enhance(self, enhancing_func):
        self.Request = enhancing_func(self.Request)

    def Request(self, method=None):
        if self.sealed: return

        if self.instance == None: 
            raise NoAttachmentException("LoustEndpoint not attached to Locust TaskSet object")
        elif method == None and type(self.methods) == str: 
            method = self.methods


        if type(method) == list and method.lower() in self.methods \
                or type(method) == str and (method.lower() == self.methods \
                or method.lower() in self.methods):
            # Get Blocks
            if   method == 'get' and self.get_body_type == None :  self.get_simple()
            elif method == 'get' and self.get_body_type == 'params' :  self.get_with_params()
            # Post Blocks
            elif method == 'post' and self.post_body_type == 'json' :  self.post_with_json()
            elif method == 'post' and self.post_body_type == 'data' :  self.post_with_data()
            elif method == 'post' and self.post_body_type == 'params' :  self.post_with_params()
            # Patch Blocks
            elif method == 'patch'   :  self.patch()
            # Delete Blocks
            elif method == 'delete'  :  self.delete()
            self.__class__.previous = self

        if len(self.methods) > 1 and method == None and type(self.methods) == list:
            err = "This endpoint supports more than one method which requires specifying it when calling the request function"
            raise MissingMethodException(err)
        elif type(self.methods) == str and self.methods != method.lower() and method is not None:
            err = "Request was called with {} but only supports {}".format(method.upper(), self.methods.upper())
            raise MissingMethodException(err)


    def get_simple(self):
        t0 = time()
        req = self.instance.client.get(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            catch_response  = True,
                            allow_redirects = self.redirects
                            )
        self.status_check(req, time() - t0)


    def get_with_params(self):
        t0 = time()
        req = self.instance.client.get(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            params          = self.body,
                            catch_response  = True,
                            allow_redirects = self.redirects
                            )
        self.status_check(req, time() - t0)


    def post_with_json(self):
        t0 = time()
        req = self.instance.client.post(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            json            = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def post_with_data(self):
        t0 = time()
        req = self.instance.client.post(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            data            = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def post_with_params(self):
        t0 = time()
        req = self.instance.client.post(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            params          = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def patch(self):
        t0 = time()
        req = self.instance.client.patch(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            json            = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def delete(self):
        t0 = time()
        req = self.instance.client.delete(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)



    def status_check(self, request_object, t):
        timeout = "Empty response, possible timeout"
        if request_object.status_code >= 200 and request_object.status_code < 400:
            self.Result = self.RequestResult(True, request_object, self.endpoint)
            request_object.success()
            self.bank_statistics(t, self.Result.success)
        elif request_object.status_code == 0:
            self.Result = self.RequestResult(False, request_object, self.endpoint)
            request_object.failure(
                "{} - {}".format(request_object.content, timeout))
        else:
            self.Result = self.RequestResult(False, request_object, self.endpoint)
            request_object.failure("{}".format(request_object.content))
        


    class RequestResult:
        def __init__(self, status, request_object, endpoint):
            """The result subclass of each request made by a LocustEndpoint"""

            self.success = status
            self.failure = not status
            self.endpoint = endpoint
            self.json    = lambda: self.content_as_json()
            
            try: self.status_code = request_object.status_code
            except: self.status_code = 0
            try: self.response = request_object.content
            except: self.response = {}

        
        def content_as_json(self):
            if self.response == {}: return {}
            try: js = loads(self.response)
            except:
                js = {}
                WARN("CANNOT CONVERT RESPONSE OF {} TO JSON".format(self.endpoint))
            finally: return js


class LocustEndpointCollection(object):
    created = 0
    def __init__(self):
        self.instances  = LocustEndpoint.instances
        self.distrib    = False
        self.unique     = self.separate_uniques()

        self.endpoint_statistics = self.frame_welder()

        if self.is_distributed(): 
            self.distrib = True
            self.resolve_distributed()

    @property
    def totals(self):
        return runners.locust_runner.stats.total.stats.num_requests
  
    def separate_uniques(self):
        uniques = dict()
        for instance in self.instances:
            if instance.endpoint in uniques.keys():
                uniques[instance.endpoint].append(instance)
            else:
                uniques[instance.endpoint] = [instance]
        return uniques

    def frame_welder(self):
        frame_collection = dict()

        for endp in self.unique:
            new_frame = pd.concat([x.statistics for x in self.unique[endp]], 
                                    ignore_index=True, sort=True)
            try:
                frame_collection[endp] = new_frame
            except KeyError: continue
        
        return frame_collection

    def is_distributed(self):
        return True if isinstance(runners.locust_runner, runners.DistributedLocustRunner) else False

    def resolve_distributed(self):
        """Only one runner from each machine will access this function 
        due to the per-machine singleton declaration making the runner a
        hub of endpoint statistics for all slaves running on the same 
        machine
        """

        runners.DistributedLocustRunner.backpackstats   = self.endpoint_statistics
        

    def __new__(cls, *args, **kwargs):
        if LocustEndpointCollection.created < 1:
            LocustEndpointCollection.created += 1
            return object.__new__(cls, *args, **kwargs)
        else: return



def _backpack_serialize_frame(client_id, data):
    try:
        serial = dict()
        leader_data = runners.DistributedLocustRunner.backpackstats
        for frame in leader_data:
            serial[frame] = leader_data[frame].to_dict()
    except AttributeError: pass
    else: data[client_id] = serial

def _backpack_extend_backpack(client_id, data):
    try: 
        runners.MasterLocustRunner.backpack[client_id] = data[client_id]
    except: pass
        
def _backpack_master_setup():
    runners.MasterLocustRunner.backpack  = dict()
    runners.MasterLocustRunner.n_clients = len(runners.locust_runner.clients)

def _backpack_stop_test():
    Insight(LocustEndpointCollection)

def _backpack_slave_stop():
    LECinst = LocustEndpointCollection()
    
@web.app.route("/backpack")
def total_content_length():
    try:
        return dumps(runners.MasterLocustRunner.backpack)
    except:
        return "Backpack Page"

events.slave_report             += _backpack_extend_backpack
events.report_to_master         += _backpack_serialize_frame
events.master_start_hatching    += _backpack_master_setup
events.master_stop_hatching     += _backpack_stop_test
events.locust_stop_hatching     += _backpack_slave_stop