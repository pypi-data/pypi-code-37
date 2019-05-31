from uuid import uuid4
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout as django_logout

import requests
import jwt

LOGIN_URL = getattr(settings, 'ISLAUTH_LOGIN_URL', 'https://auth.isl.co/auth/login/')
TOKEN_ENDPOINT = getattr(settings, 'ISLAUTH_TOKEN_ENDPOINT', 'https://auth.isl.co/auth/token/')


def generate_redirect_uri(request):
    path = reverse('islauth_callback')
    return '%s://%s%s' % (
        'https' if request.is_secure() else 'http', request.META['HTTP_HOST'], path)


def login(request):
    request.session['next'] = request.GET.get('next', None)

    request.session['secret'] = str(uuid4())

    params = {
        'redirect_uri': generate_redirect_uri(request),
        'secret': request.session['secret'],
    }

    return HttpResponseRedirect(
        "%s?%s" % (LOGIN_URL, urlencode(params)))


def callback(request):
    if request.session.get('secret', None) is None:
        return HttpResponse('Invalid callback', status=401)

    params = {
        'redirect_uri': generate_redirect_uri(request),
        'secret': request.session['secret'],
    }

    resp = requests.post(TOKEN_ENDPOINT, data=params)
    if resp.status_code != 200:
        return HttpResponse('Invalid token response', status=401)

    tokens = resp.json()
    id_token = jwt.decode(
        tokens['id_token'].encode('utf-8'),
        request.session['secret'],
        algorithms=['HS256'],
        verify=False
    )

    email = id_token.get('email', None)
    if email is None:
        return HttpResponse('Invalid Data', status=401)

    user = auth.authenticate(email=email)
    if not user:
        return HttpResponse('User account not found', status=404)
    auth.login(request, user)

    redirect = request.session.get('next', None)
    redirect_default = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    return HttpResponseRedirect(redirect or redirect_default)


def logout(request):
    return django_logout(request)
