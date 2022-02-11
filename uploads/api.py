from django.urls import path

from .views import ApiGetUploadToRenderJson, ApiUploadResultJson


urlpatterns = [

    path('v1/get_upload_to_render/',
         ApiGetUploadToRenderJson.as_view(), name='api_v1_get_upload'),
    path('v1/upload_result/', ApiUploadResultJson.as_view(),
         name='api_v1_upload_result'),

]
