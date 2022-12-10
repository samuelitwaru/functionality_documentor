from re import compile

from django.conf import settings
from django.http import HttpResponseRedirect

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # if request.user.is_authenticated)
        response = self.get_response(request)
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            print(path, any(m.match(path) for m in EXEMPT_URLS))
            if not any(m.match(path) for m in EXEMPT_URLS):
                # return response
                return HttpResponseRedirect(settings.LOGIN_URL)

        # Code to be executed for each request/response after
        # the view is called.

        return response
