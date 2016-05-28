from html2text import html2text

from django.conf import  settings
from django.core.mail import send_mail, get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.template import loader


def send_templated_mail(subject, template, context, to):
    t = loader.get_template(template)
    send_mail(subject, t.render(context), settings.DEFAULT_FROM_EMAIL, to, fail_silently=True)


def send_mass_html_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    messages = []
    for subject, message, sender, recipient in datatuple:
        plain_message = html2text(message)
        mail = EmailMultiAlternatives(subject, plain_message, sender, recipient,
                             connection=connection)
        mail.attach_alternative(message, 'text/html')
        messages.append(mail)
    return connection.send_messages(messages)
