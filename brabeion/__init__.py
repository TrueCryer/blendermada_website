from brabeion.sites import badges

from django.utils.module_loading import autodiscover_modules


def autodiscover():
    autodiscover_modules('badges')
