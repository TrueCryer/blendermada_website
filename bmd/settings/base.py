import os

from django.core.urlresolvers import reverse_lazy
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# URL

ROOT_URLCONF = 'bmd.urls.base'


# Database

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}


SECRET_KEY = "secret"


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'accounts',
    'captcha',
    'core',
    'mailing',
    'materials',
    'profiles',
    'smuggler',
    'uploads',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

WSGI_APPLICATION = 'bmd.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'


# Sites

SITE_ID = 1


# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


# E-Mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Blendermada] '

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'foo@bar.net'


# Registration

ACCOUNT_ACTIVATION_DAYS = 7


# Login

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('account_home')


# Auth

AUTHENTICATION_BACKENDS = (
    'accounts.backends.CaseInsensitiveModelBackend',
)


# Captcha

CAPTCHA_FONT_SIZE = 28
CAPTCHA_LETTER_ROTATION = (-40, 40)
CAPTCHA_LENGTH = 8


# Smuggler

SMUGGLER_EXCLUDE_LIST = [
    'contenttypes.contenttype',
    'sessions.session',
    'auth.permission',
    'admin.logentry',
]
