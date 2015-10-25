from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import (
    ActivationView, RegistrationView,
    login, logout,
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete,
    password_change, password_change_done,
    HomeView, StatisticsView, MaterialsView, SettingsView, UploadsView,
)


urlpatterns = [
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='accounts/activation_complete.html'),
        name='registration_activation_complete'),

    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='accounts/registration_complete.html'),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(template_name='accounts/registration_closed.html'),
        name='registration_disallowed'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^password/change/$', password_change, name='password_change'),
    url(r'^password/change/done/$', password_change_done, name='password_change_done'),
    url(r'^password/reset/$', password_reset, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/done/$', password_reset_done, name='password_reset_done'),

    url(r'^home/$', HomeView.as_view(), name='account_home'),
    url(r'^materials/$', MaterialsView.as_view(), name='account_materials'),
    url(r'^statistics/$', StatisticsView.as_view(), name='account_statistics'),
    url(r'^notifications/$', SettingsView.as_view(), name='account_settings'),
    url(r'^uploads/$', UploadsView.as_view(), name='account_uploads'),
]
