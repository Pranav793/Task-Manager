import time
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse

from tasks.models import Task
from datetime import datetime, timedelta

from celery.decorators import periodic_task

from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=60))
def send_email_reminder():
    print("Starting to process Emails")
    for user in User.objects.all():
        pending_qs = Task.objects.filter(deleted=False, user=user, completed=False)
        email_content = f"You have {pending_qs.count()} Pending Tasks"
        send_mail("Pending Tasks from Tasks Manager", email_content, "tasks@tasks_manager.org", [user.email])
        print(f"Completed Processing User {user.id}")



@app.task
def test_background_jobs():
    print("This is from the bg")
    for i in range(10):
        time.sleep(1)
        print(i)