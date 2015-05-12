from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


class JsonResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        return HttpResponse(json.dumps(context), content_type='application/json')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
