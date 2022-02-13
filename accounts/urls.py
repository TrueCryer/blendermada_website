from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from .views import (
    ActivationView, RegistrationView,
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView,
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


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('home/', HomeView.as_view(), name='account_home'),
    path('materials/', MaterialsView.as_view(), name='account_materials'),
    path('statistics/', StatisticsView.as_view(), name='account_statistics'),
    path('notifications/', SettingsView.as_view(), name='account_settings'),
    path('uploads/', UploadsView.as_view(), name='account_uploads'),

    path('apikey/generate/',
         GenerateApikeyView.as_view(), name='account_generate_apikey'),

]
