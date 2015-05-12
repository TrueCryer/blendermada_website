from __future__ import unicode_literals

from django.conf import settings


REGISTRATION_OPEN = getattr(settings, 'REGISTRATION_OPEN', True)
SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 7)
REGISTRATION_EMAIL_SUBJECT_PREFIX = getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '')
