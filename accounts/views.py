from __future__ import unicode_literals

from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, RedirectView

from core.views import LoginRequiredMixin
from profiles.models import UserProfile

from .forms import (
    RegistrationForm,
    AuthenticationFormBootstrap,
    PasswordResetFormBootstrap,
    SetPasswordFormBootstrap,
    PasswordChangeFormBootstrap,
    SettingsForm,
)
from .models import RegistrationProfile, ApiKey
from .settings import REGISTRATION_OPEN, SEND_ACTIVATION_EMAIL


class RegistrationView(FormView):
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'accounts/registration_form.html'

    def dispatch(self, *args, **kwargs):
        if not self.registration_allowed(self.request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(self.request, **form.cleaned_data)
        success_url = self.get_success_url(self.request, new_user)
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def registration_allowed(self, request):
        return REGISTRATION_OPEN

    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email1'], cleaned_data['password1']
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, cleaned_data,
            send_email=SEND_ACTIVATION_EMAIL,
            request=request,
        )
        return new_user

    def get_success_url(self, request, user):
        return ('registration_complete', (), {})


class ActivationView(TemplateView):
    http_method_names = ['get']
    template_name = 'accounts/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, activation_key):
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})


def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('account_home'))
    return auth_views.login(request, template_name='accounts/login.html', authentication_form=AuthenticationFormBootstrap)


def logout(request):
    if not request.user.is_authenticated():
        return redirect(reverse('home'))
    return auth_views.logout(request, template_name='accounts/logout.html')


def password_reset(request):
    if request.user.is_authenticated():
        return redirect(reverse('account_home'))
    return auth_views.password_reset(request,
        post_reset_redirect=reverse('password_reset_done'),
        template_name='accounts/password_reset_form.html',
        password_reset_form=PasswordResetFormBootstrap,
    )


def password_reset_done(request):
    return auth_views.password_reset_done(request,
        template_name='accounts/password_reset_done.html',
    )


def password_reset_confirm(request, uidb64, token):
    return auth_views.password_reset_confirm(request, uidb64, token,
        template_name='accounts/password_reset_confirm.html',
        set_password_form=SetPasswordFormBootstrap,
        post_reset_redirect=reverse('password_reset_complete'),
    )


def password_reset_complete(request):
    return auth_views.password_reset_complete(request,
        template_name='accounts/password_reset_complete.html',
    )


def password_change(request):
    return auth_views.password_change(request,
        template_name='accounts/password_change_form.html',
        password_change_form=PasswordChangeFormBootstrap,
        post_change_redirect=reverse('password_change_done'),
    )


def password_change_done(request):
    return auth_views.password_change_done(request,
        template_name='accounts/password_change_done.html',
    )


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_home.html'


class MaterialsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_materials.html'


class UploadsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_uploads.html'


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_statistics.html'


class SettingsView(LoginRequiredMixin, FormView):
    form_class = SettingsForm
    template_name = 'accounts/account_settings.html'
    success_url = reverse_lazy('account_home')

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        UserProfile.objects.filter(user=self.request.user).update(
            country = form.cleaned_data['country'],
            send_newsletters = form.cleaned_data['send_newsletters'],
            send_notifications = form.cleaned_data['send_notifications'],
            show_fullname = form.cleaned_data['show_fullname'],
            show_email = form.cleaned_data['show_email'],
            about = form.cleaned_data['about'],
            website = form.cleaned_data['website'],
            deviantart = form.cleaned_data['deviantart'],
            facebook = form.cleaned_data['facebook'],
            twitter = form.cleaned_data['twitter'],
            gplus = form.cleaned_data['gplus'],
        )
        return super(SettingsView, self).form_valid(form)

    def get_initial(self):
        user = self.request.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'country': user.profile.country,
            'send_newsletters': user.profile.send_newsletters,
            'send_notifications': user.profile.send_notifications,
            'show_fullname': user.profile.show_fullname,
            'show_email': user.profile.show_email,
            'about': user.profile.about,
            'website': user.profile.website,
            'deviantart': user.profile.deviantart,
            'facebook': user.profile.facebook,
            'twitter': user.profile.twitter,
            'gplus': user.profile.gplus,
        }


class GenerateApikeyView(LoginRequiredMixin, RedirectView):
    pattern_name = 'account_home'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        key, created = ApiKey.objects.get_or_create(user=self.request.user)
        key.generate()
        key.send_key_email()
        return super(GenerateApikeyView, self).get_redirect_url(*args, **kwargs)
