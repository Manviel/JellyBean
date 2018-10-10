from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

from celery import shared_task


@shared_task
def email_greet(mail):
    subject = 'Thank you for registering to our site'
    message = 'it  means a world to us'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mail, ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('home')
