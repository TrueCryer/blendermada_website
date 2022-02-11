from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    ActivationView, RegistrationView,
    login, logout,
    password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete,
    password_change, password_change_done,
    HomeView, StatisticsView, MaterialsView, SettingsView, UploadsView,
    GenerateApikeyView,
)


urlpatterns = [

    path('activate/<activation_key>/',
         ActivationView.as_view(),
         name='registration_activate'),

    path('activate/complete/',
         TemplateView.as_view(
            template_name='accounts/activation_complete.html',
             ),
         name='registration_activation_complete'),

    path('register/',
         RegistrationView.as_view(),
         name='registration_register'),

    path('register/complete/',
         TemplateView.as_view(
            template_name='accounts/registration_complete.html',
             ),
         name='registration_complete'),
    path('register/closed/',
         TemplateView.as_view(
            template_name='accounts/registration_closed.html',
             ),
         name='registration_disallowed'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('password/change/',
         password_change, name='password_change'),

    path('password/change/done/',
         password_change_done, name='password_change_done'),

    path('password/reset/',
         password_reset, name='password_reset'),

    path('password/reset/confirm/<uidb64>/<token>/',
         password_reset_confirm, name='password_reset_confirm'),

    path('password/reset/complete/',
         password_reset_complete, name='password_reset_complete'),

    path('password/reset/done/',
         password_reset_done, name='password_reset_done'),

    path('home/', HomeView.as_view(), name='account_home'),
    path('materials/', MaterialsView.as_view(), name='account_materials'),
    path('statistics/', StatisticsView.as_view(), name='account_statistics'),
    path('notifications/', SettingsView.as_view(), name='account_settings'),
    path('uploads/', UploadsView.as_view(), name='account_uploads'),

    path('apikey/generate/',
         GenerateApikeyView.as_view(), name='account_generate_apikey'),

]
