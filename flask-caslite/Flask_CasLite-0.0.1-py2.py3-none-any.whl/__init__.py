
import os
from importlib import import_module
from .cas import login_required, handle_logout 



class CasLite(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app, url_prefix=None):

        # Basic
        

        # Cas Server
        app.config.setdefault('CAS_SERVER', 'https://join.byd.com/casoa')
        app.config.setdefault('CAS_VERSION', 'v2')
        app.config.setdefault('CAS_TOKEN_SESSION_KEY', '_CAS_TOKEN')
        app.config.setdefault('CAS_USERNAME_SESSION_KEY', 'CAS_USERNAME')
        app.config.setdefault('CAS_ATTRIBUTES_SESSION_KEY', 'CAS_ATTRIBUTES')




