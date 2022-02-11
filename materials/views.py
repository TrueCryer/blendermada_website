from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone
from django.views.generic import DetailView, ListView

from core.views import JsonResponseMixin, APIKeyMixin

from .models import Category, Material, Statistic, Vote
from . import settings


def index(request):
    queries_without_page = request.GET.copy()
    queries_without_num = request.GET.copy()
    if 'page' in queries_without_page.keys():
        del queries_without_page['page']
    if 'num' in queries_without_num.keys():
        del queries_without_num['num']
    kw = dict()
    engine = request.GET.get('engine', '')
    category = request.GET.get('category', '')
    keyword = request.GET.get('keyword', '')
    if engine != '':
        kw['engine'] = engine
    if category != '':
        kw['category__slug'] = category
    if keyword != '':
        kw['name__icontains'] = keyword
    materials = Material.objects.published(**kw).select_related('category')
    num = request.GET.get('num')
    try:
        num = int(num)
    except TypeError:
        num = settings.MATERIALS_PER_PAGE
    paginator = Paginator(materials, num)
    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    t = loader.get_template('materials/list.html')
    c = {
        'request': request,
        'page': page,
        'num': num,
        'queries_without_page': queries_without_page,
        'queries_without_num': queries_without_num,
        'engine': engine,
        'category': category,
        'keyword': keyword,
    }
    return HttpResponse(t.render(c))


class MaterialDetailView(DetailView):
    queryset = Material.objects.published()
    template_name = 'materials/detail.html'


class MaterialDownloadView(DetailView):
    queryset = Material.objects.published()

    def get(self, request, *args, **kwargs):
        mat = self.get_object()
        stat, created = Statistic.objects.get_or_create(
            material=mat, date=timezone.now()
        )
        if not created:
            stat.count += 1
            stat.save()
        return HttpResponse(
            mat.storage.read(), content_type='application/blender')


@login_required
def vote(request, pk, slug, score):
    mat = get_object_or_404(Material, pk=pk, slug=slug)
    voting, created = Vote.objects.get_or_create(
        user=request.user, material=mat, defaults={'score': score},
    )
    if not created:
        voting.score = score
        voting.save()
    return HttpResponseRedirect(reverse(
        'materials:detail', kwargs={'pk': pk, 'slug': slug}))


# API

class ArgumentsMixin(object):
    mapping = None

    def dispatch(self, request, *args, **kwargs):
        self.parse_arguments()
        return super(ArgumentsMixin, self).dispatch(request, *args, **kwargs)

    def parse_arguments(self):
        if self.mapping is None:
            raise ImproperlyConfigured("%(cls)s is missing a mapping." % {
                                                'cls': self.__class__.__name__
                                        })
        self.arguments = {}
        get_keys = self.request.GET.keys()
        for key, target in self.mapping:
            if key in get_keys:
                self.arguments[target] = self.request.GET[key]
        self.kwargs.update(self.arguments)

    def get_queryset(self):
        queryset = super(ArgumentsMixin, self).get_queryset()
        return queryset.filter(**self.arguments)


class ApiFullJson(JsonResponseMixin, ArgumentsMixin, ListView):
    queryset = Material.objects.published()
    mapping = (
        ('engine', 'engine'),
    )

    def get_context_data(self, **kwargs):
        categories = [{'id': cat.pk,
                       'slug': cat.slug,
                       'name': cat.name} for cat in Category.objects.all()]
        materials = [{'id': mat.pk,
                      'slug': mat.slug,
                      'category': mat.category.name,
                      'name': mat.name,
                      'description': mat.text_description,
                      'downloads': mat.downloads,
                      'rating': mat.rating,
                      'votes': mat.votes_count,
                      'image': mat.thumb_medium.url,
                      'storage': mat.get_download_url(),
                      'storage_name': mat.storage_name} for mat in self.object_list]
        return {'categories': categories, 'materials': materials}


class ApiMaterialListJson(JsonResponseMixin, ArgumentsMixin, ListView):
    queryset = Material.objects.published()
    mapping = (
        ('engine', 'engine'),
        ('category', 'category_id'),
        ('author', 'user_id'),
    )

    def get_context_data(self, **kwargs):
        answer = [{'id': mat.pk,
                   'slug': mat.slug,
                   'name': mat.name} for mat in self.object_list]
        return answer


class ApiCategoryListJson(JsonResponseMixin, ArgumentsMixin, ListView):
    model = Category
    mapping = ()

    def get_context_data(self, **kwargs):
        answer = [{'id': cat.pk,
                   'slug': cat.slug,
                   'name': cat.name} for cat in self.object_list]
        return answer


class ApiMaterialDetailJson(JsonResponseMixin, ArgumentsMixin, DetailView):
    queryset = Material.objects.published()
    mapping = (
        ('id', 'pk'),
        ('slug', 'slug'),
    )

    def get_context_data(self, **kwargs):
        mat = self.object
        context = {
            'id': mat.pk,
            'slug': mat.slug,
            'name': mat.name,
            'description': mat.text_description,
            'downloads': mat.downloads,
            'rating': mat.rating,
            'votes': mat.votes_count,
            'image': mat.thumb_small.url,
            'storage': mat.get_download_url(),
            'storage_name': mat.storage_name,
        }
        return context


class ApiStatisticsJson(JsonResponseMixin, ArgumentsMixin, ListView):
    model = Statistic
    mapping = ()

    def get_context_data(self, **kwargs):
        context = [
            {'date': stat.date.strftime('%Y-%m-%d'),
             'material': stat.material.pk,
             'count': stat.count} for stat in self.object_list
        ]
        return context


class ApiFavoritesJson(JsonResponseMixin, APIKeyMixin, ArgumentsMixin,
                       ListView):
    queryset = Material.objects.published()
    mapping = (
        ('engine', 'engine'),
    )

    def get_queryset(self):
        queryset = super(ApiFavoritesJson, self).get_queryset()
        queryset = queryset.filter(
            pk__in=self.api_user.favorites.all().values_list(
                'material__pk', flat=True))
        return queryset.filter(**self.arguments)

    def get_context_data(self, **kwargs):
        answer = [{'id': mat.pk,
                   'slug': mat.slug,
                   'name': mat.name} for mat in self.object_list]
        return answer


class ApiCommentNotify(JsonResponseMixin, DetailView):
    model = Material

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.send_comment_notification()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {'response': 200}
