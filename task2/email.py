from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_review_email(name, email, task, time):

    context = {
        'name': name,
        'email': email,
        'task': task,
        'time': time
    }

    email_subject = 'Good Job!, You just added a task'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)

def send_reminder_email(name, email, task, time):

    context = {
        'name': name,
        'email': email,
        'task': task,
        'time': time
    }

    email_subject = 'Hey there !, You have a deadline to meet'
    email_body = render_to_string('reminder_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)

def send_otp_email(name, email, group_name, otp):
    context = {
        'name': name,
        'email': email,
        'group': group_name,
        'otp': otp
    }

    email_subject = "Welcome to Group To Do List"
    email_body = render_to_string('otp.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)
