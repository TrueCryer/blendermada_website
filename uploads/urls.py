from django.conf.urls import url

from .views import UploadView, UploadDetailView, StuffView, UploadApproveView


app_name = 'uploads'

urlpatterns = [

    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^detail/(?P<pk>\d+)/$', UploadDetailView.as_view(), name='detail'),
    url(r'^approve/(?P<pk>\d+)/$', UploadApproveView.as_view(), name='approve'),
    url(r'^stuff/$', StuffView.as_view(), name='stuff')

]
