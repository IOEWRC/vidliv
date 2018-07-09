from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.conf import settings
from django.shortcuts import redirect


EXEMPT_VIEWS = getattr(settings, 'LOGIN_EXEMPT_VIEWS', []) + [settings.LOGIN_URL, ]


class LoginRequiredMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.is_ajax():
            assert hasattr(request, 'user')
            resolve_obj = resolve(request.path_info)
            request_view = resolve_obj.namespace + ':' + resolve_obj.url_name if resolve_obj.namespace else resolve_obj.url_name
            if request.user.is_authenticated and (request_view in EXEMPT_VIEWS):
                return redirect(settings.LOGIN_REDIRECT_URL)
            elif request.user.is_authenticated or (request_view in EXEMPT_VIEWS):
                return None
            else:
                return HttpResponseRedirect(reverse('auth_login') + '?next=' + request.path_info)
