from django.shortcuts import redirect

from .lib import coverpage_is_available, get_coverpage_conf


def CoverPageMiddleware(get_response):
    def middleware(request):
        config, active, url, cookiename = get_coverpage_conf()

        # do redirect if applicable
        if active and \
           cookiename not in request.COOKIES and \
           request.method == 'GET' and \
           not request.is_ajax() and \
           request.path != url and \
           coverpage_is_available(request):
                response = redirect(url)
                response.set_cookie(
                    '%s_referrer' % cookiename,
                    request.path
                )
                return response

        # fallback, i.e. do not show coverpage
        response = get_response(request)
        return response

    return middleware
