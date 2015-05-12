from django.conf import settings


MATERIALS_PER_PAGE = getattr(settings, 'MATERIALS_PER_PAGE', 12)
