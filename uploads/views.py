import base64

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, DetailView, ListView
from django.views.decorators.csrf import csrf_exempt


from core.views import JsonResponseMixin, LoginRequiredMixin

from .forms import UploadForm
from .models import Upload, Scene
from .settings import UPLOADS_SECRET_KEY


class SecretKeyMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            if not (request.META['HTTP_SECRET'] == UPLOADS_SECRET_KEY):
                return HttpResponseForbidden('You have no access to this')
        except KeyError:
            return HttpResponseForbidden('You have no access to this')
        return super(SecretKeyMixin, self).dispatch(request, *args, **kwargs)


class UploadView(LoginRequiredMixin, FormView):
    template_name = 'uploads/upload.html'
    form_class = UploadForm
    success_url = reverse_lazy('account_uploads')

    def dispatch(self, request, *args, **kwargs):
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UploadView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save_data()
        return super(UploadView, self).form_valid(form)


class UploadDetailView(LoginRequiredMixin, DetailView):
    model = Upload
    template_name = 'uploads/detail.html'

    def get_queryset(self):
        queryset = super(UploadDetailView, self).get_queryset()
        return queryset.filter(author=self.request.user)


class UploadApproveView(LoginRequiredMixin, DetailView):
    model = Upload

    def get_queryset(self):
        queryset = super(UploadApproveView, self).get_queryset()
        return queryset.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user_approved = True
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class StuffView(ListView):
    model = Scene
    template_name = 'uploads/stuff.html'


# ###
# API Definitions

class ApiGetUploadToRenderJson(SecretKeyMixin, JsonResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        try:
            upload = Upload.objects.pop_next_to_render()
        except Upload.DoesNotExist:
            raise Http404('Nothing to render')
        answer = {
            'id': upload.pk,
            'name': upload.name,
            'description': upload.description,
            'name_in_file': upload.name_in_file,
            'uploaded_file': base64.b64encode(upload.uploaded_file.read()).decode('utf-8'),
            'scene': upload.scene,
            'engine': upload.engine,
            'author': upload.author.username,
        }
        return answer


class  ApiUploadResultJson(SecretKeyMixin, JsonResponseMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        upload = get_object_or_404(Upload, pk=request.POST['id'], status__in=['w', 'r'])
        upload.render_finished = timezone.now()
        try:
            upload.storage = request.FILES['storage.blend']
        except KeyError:
            pass
        try:
            upload.image = request.FILES['image.png']
        except KeyError:
            pass
        upload.error = request.POST['error']
        if upload.error:
            upload.status = 'e'
        else:
            upload.status = 'a'
        upload.save()
        upload.mail_about_ready()
        return HttpResponseForbidden('Test forbidden')
