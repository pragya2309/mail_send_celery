from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task
from celery_project import settings
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task


@shared_task(bind=True)
def send_mail_fun(self,email):
    
    users = get_user_model().objects.all()
    print(users)
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message =  " I'm testing the celery module......."

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [email],
            fail_silently = False,
            
        )
    return "Done"


@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


