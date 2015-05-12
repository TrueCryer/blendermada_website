from django.conf import  settings
from django.core.mail import send_mail
from django.template import Context, loader


def send_templated_mail(subject, template, context, to):
    t = loader.get_template(template)
    c = Context(context)
    send_mail(subject, t.render(c), settings.DEFAULT_FROM_EMAIL, to, fail_silently=True)