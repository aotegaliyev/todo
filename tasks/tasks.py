import logging
from datetime import datetime
from smtplib import SMTPException
from time import sleep

from celery import shared_task
from django.core.mail import send_mail
from todo import settings

from .models import Task

logger = logging.getLogger('django-error')


@shared_task
def send_deadline_notification():
    tasks = Task.objects.select_related('author').filter(
        deadline__isnull=False,
        author__isnull=False,
        author__email__isnull=False,
        deadline__gte=datetime.now(),
        notify_sent=False,
    )
    for task in tasks:
        date_difference = (task.deadline - datetime.now()).total_seconds() / 60.0
        if 0 < date_difference <= 60:
            try:
                send_mail(
                    'Уведомление о дедлайне',
                    'Осталось 1 час до завершение задачи: {}'.format(task.title),
                    settings.DEFAULT_FROM_EMAIL,
                    [task.author.email],
                    fail_silently=False,
                )

                task.notify_sent = True
                task.save()
            except SMTPException as exc:
                logger.exception(exc)

    sleep(10)


@shared_task
def send_async_notification(task):
    try:
        send_mail(
            'Уведомление о дедлайне',
            'Осталось 1 час до завершение задачи: {}'.format(task.title),
            settings.DEFAULT_FROM_EMAIL,
            [task.author.email],
            fail_silently=False,
        )

        task.notify_sent = True
        task.save()
    except SMTPException as exc:
        logger.exception(exc)
