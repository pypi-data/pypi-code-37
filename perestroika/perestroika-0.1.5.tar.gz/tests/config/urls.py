from django.urls import path, include

from test_django.urls import urlpatterns as test_urls

urlpatterns = [
    path('test/', include(test_urls)),
]
