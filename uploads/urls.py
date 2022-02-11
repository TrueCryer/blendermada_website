from django.urls import path

from .views import UploadView, UploadDetailView, StuffView, UploadApproveView


app_name = 'uploads'

urlpatterns = [

    path('upload/', UploadView.as_view(), name='upload'),
    path('detail/<int:pk>/', UploadDetailView.as_view(), name='detail'),
    path('approve/<int:pk>/', UploadApproveView.as_view(), name='approve'),
    path('stuff/', StuffView.as_view(), name='stuff')

]
