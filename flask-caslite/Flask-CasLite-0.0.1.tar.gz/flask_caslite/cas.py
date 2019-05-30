# -*- coding: utf-8 -*-
"""
    :author: jooonwood
    :license: MIT, see LICENSE for more details.
"""
from functools import wraps
from xmltodict import parse
try:
    from urllib import urlopen,urlencode
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import urlencode

from flask import current_app, redirect, request, session

class CasClient:

    def generate_service_url(base_url,args):
        query = args.to_dict()
        query.pop('ticket', None)
        return base_url+'?{0}'.format(urlencode(query))

    def validate_cas_v1(cas_server,service_url,ticket):
        xmldump = urlopen(cas_server + '/validate?ticket='+ticket+'&service='+service_url).read().strip().decode('utf8', 'ignore')
        info = xmldump.split('\n')
        if info[0] == 'yes':
            return { 'username':info[1] }
        return None

    def validate_cas_v2(cas_server,service_url,ticket):
        try:
            xmldump = urlopen(cas_server + '/serviceValidate?ticket='+ticket+'&service='+service_url).read().strip().decode('utf8', 'ignore')
            xml_to_dict = parse(xmldump)
            isValid = True if 'cas:authenticationSuccess' in xml_to_dict['cas:serviceResponse'] else False
        except ValueError:
            return None

        if isValid:
            cas_user = xml_to_dict['cas:serviceResponse']['cas:authenticationSuccess']
            username = cas_user.get('cas:user')
            attributes = cas_user.get('cas:attributes')
            
            if attributes and 'cas:memberOf' in attributes:
                attributes['cas:memberOf'] = attributes['cas:memberOf'].lstrip('[').rstrip(']').split(',')
                for group_number in range(0, len(attributes['cas:memberOf'])):
                    attributes['cas:memberOf'][group_number] = attributes['cas:memberOf'][group_number].lstrip(' ').rstrip(' ')
            return {'username' : username, 'attributes' : attributes}

        return None


def handle_logout(req):
    if req.form.get('logoutRequest'):
        logout_request = parse(request.form['logoutRequest'])
        ticket = logout_request.get('samlp:LogoutRequest', {}).get('samlp:SessionIndex')
        return ticket
        

def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        sess_username = current_app.config['CAS_USERNAME_SESSION_KEY']
        if sess_username in session:
            return function(*args, **kwargs)

        sess_ticket = current_app.config['CAS_TOKEN_SESSION_KEY']
        sess_attributes = current_app.config['CAS_ATTRIBUTES_SESSION_KEY']
        cas_server = current_app.config['CAS_SERVER']
        cas_version = current_app.config['CAS_VERSION']

        ticket = request.args.get('ticket',None)
        service_url = CasClient.generate_service_url(request.base_url,request.args)

        if ticket:
            user = getattr(CasClient, 'validate_cas_' + cas_version)(cas_server,service_url,ticket)
            if user is not None:
                session[sess_ticket] = ticket
                session[sess_username] = user.get('username')
                session[sess_attributes] = user.get('attributes')
                return function(*args, **kwargs)
        return redirect(cas_server + '/login?service='+service_url)     
    return wrap




