from celery import shared_task
from time import sleep


@shared_task
def send_mail_task():
    sleep(5)
    return {"status": "ok"}
