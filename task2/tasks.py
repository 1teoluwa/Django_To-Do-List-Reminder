# from celery.decorators import task
from celery import shared_task
from celery.utils.log import get_task_logger
from .email import send_review_email, send_reminder_email, send_otp_email
# from task2.forms import TaskForm
from celery import shared_task
from django.core.mail import send_mail
from .models import TaskModel

logger = get_task_logger(__name__)


# @task(name="send_review_email_task")
@shared_task
def send_review_email_task(name, email, task, time):
    logger.info("Sent review email")
    return send_review_email(name, email, task, time)


# @staticmethod
@shared_task
def send_email_reminder_task(task_id):
    task = TaskModel.objects.get(pk=task_id)
    name = task.name
    task_content = task.task
    email = task.email
    time = task.time
    logger.info("Sent reminder email")
    return send_reminder_email(name, email, task_content, time)

@shared_task
def email_otp(name,email, group_name, otp):
    # logger.info("Sent group email")
    print(f"Sending OTP {otp} to {email} for user {name}")
    return send_otp_email(name, email, group_name, otp)