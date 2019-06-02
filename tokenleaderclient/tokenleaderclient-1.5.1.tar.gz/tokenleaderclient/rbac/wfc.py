import uuid
# import base64
from flask import request
from datetime import datetime
import json
class WorkFuncContext():
    username = ''
    org = ''
    orgunit = ''
    department = ''
    name = ''
    email = ''
    request_id = ''
    time_stamp = ''
    client_address = ''
    roles = []
    
    def get_client_address(self):
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            c = request.environ.get('REMOTE_ADDR')
        else:
            c= request.environ.get('HTTP_X_FORWARDED_FOR')            
        return c
    
    def setcontext(self, uname, em, wfc):
        self.username = uname
        self.email = em
        self.request_id = str(uuid.uuid4())
        self.time_stamp = datetime.utcnow()
        self.client_address = self.get_client_address()
        self.org = wfc.get('org')
        self.orgunit = wfc.get('orgunit')
        self.department = wfc.get('department')
        self.name = wfc.get('name')
        self.roles = wfc.get('roles')
        
    def to_dict(self):
        wfc_dict = {"username": self.username,
                    "org": org,
                    "orgunit": orgunit,
                    "department": department,
                    "name": name,
                    "email": email,
                    "request_id": request_id,
                    "time_stamp": time_stamp,
                    "client_address": client_address,
                    "roles": roles}
        return wfc_dict
    
    def to_json(self):
        j = json.dumps(self.to_dict())
        return j
        
        
                  
        
    
    
    