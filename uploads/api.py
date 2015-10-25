from django.conf.urls import url

from .views import ApiGetUploadToRenderJson, ApiUploadResultJson


urlpatterns = [

    url(r'^v1/get_upload_to_render/$', ApiGetUploadToRenderJson.as_view(), name='api_v1_get_upload'),
    url(r'^v1/upload_result/$', ApiUploadResultJson.as_view(), name='api_v1_upload_result'),

]
