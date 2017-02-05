import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from accounts.models import ApiKey


class JsonResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        return HttpResponse(json.dumps(context), content_type='application/json')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class APIKeyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not 'key' in request.GET.keys():
            return HttpResponseForbidden('Request without key')
        try:
            key = ApiKey.objects.get(key=request.GET['key'])
        except ApiKey.DoesNotExist:
            return HttpResponseForbidden('Key not found')
        self.api_user = key.user
        return super(APIKeyMixin, self).dispatch(request, *args, **kwargs)
