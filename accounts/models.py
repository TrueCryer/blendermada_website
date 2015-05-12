from __future__ import unicode_literals

import hashlib
import random
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import six, timezone
from django.utils.encoding import python_2_unicode_compatible

from profiles.models import UserProfile

from .settings import REGISTRATION_EMAIL_SUBJECT_PREFIX, ACCOUNT_ACTIVATION_DAYS


SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):

    def activate_user(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False

    def create_inactive_user(self, username, email, password, cleaned_data,
                             send_email=True, request=None):
        new_user = get_user_model().objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.first_name = cleaned_data['first_name']
        new_user.last_name = cleaned_data['last_name']
        new_user.save()

        UserProfile.objects.filter(user=new_user).update(
            country = cleaned_data['country'],
            send_notifications = cleaned_data['send_notifications'],
            send_newsletters = cleaned_data['send_newsletters'],
            show_fullname = cleaned_data['show_fullname'],
            show_email = cleaned_data['show_email'],
        )

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(request)

        return new_user

    def create_profile(self, user):
        salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
        salt = salt.encode('ascii')
        username = user.username
        if isinstance(username, six.text_type):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)

    def delete_expired_users(self):
        for profile in self.all():
            try:
                if profile.activation_key_expired():
                    user = profile.user
                    if not user.is_active:
                        user.delete()
                    profile.delete()
            except get_user_model().DoesNotExist:
                profile.delete()


@python_2_unicode_compatible
class RegistrationProfile(models.Model):
    ACTIVATED = "ALREADY_ACTIVATED"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, verbose_name='User', blank=True, null=True)
    activation_key = models.CharField('Activation key', max_length=40)

    objects = RegistrationManager()

    class Meta:
        verbose_name = 'Registration profile'
        verbose_name_plural = 'Registration profiles'

    def __str__(self):
        return 'Registration information for {}'.format(self.user)

    def activation_key_expired(self):
        expiration_date = timezone.timedelta(days=ACCOUNT_ACTIVATION_DAYS)
        return (self.activation_key == self.ACTIVATED or
                (self.user.date_joined + expiration_date <= timezone.now()))
    activation_key_expired.boolean = True

    def send_activation_email(self, request=None):
        ctx_dict = {}
        if request is not None:
            ctx_dict = RequestContext(request, ctx_dict)
        ctx_dict.update({
            'site': get_current_site(request),
            'user': self.user,
            'activation_key': self.activation_key,
            'expiration_days': ACCOUNT_ACTIVATION_DAYS,
        })
        subject = REGISTRATION_EMAIL_SUBJECT_PREFIX + render_to_string('accounts/activation_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('accounts/activation_email.txt', ctx_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.user.email])

        try:
            message_html = render_to_string('accounts/activation_email.html', ctx_dict)
        except TemplateDoesNotExist:
            message_html = None

        if message_html:
            email_message.attach_alternative(message_html, 'text/html')

        email_message.send()
