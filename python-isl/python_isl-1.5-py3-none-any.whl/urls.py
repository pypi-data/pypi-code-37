from django.conf.urls import url
from pythonisl.views import login, callback, logout

urlpatterns = [
    url(r'^login/$', login, name='islauth_login'),
    url(r'^auth/callback/$', callback, name='islauth_callback'),
    url(r'^logout/$', logout, name='islauth_logout'),
]
