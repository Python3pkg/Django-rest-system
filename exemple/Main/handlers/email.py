from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_email(template, subject, dict, user):
    rendered = render_to_string("emails/" + template, dict)

    msg = EmailMultiAlternatives(subject, rendered, "no-reply@g4brym.ovh", [user]) # user.email
    msg.attach_alternative(rendered, "text/html")
    msg.send(True)