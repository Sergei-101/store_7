# tasks.py
import asyncio
from celery import shared_task
from telegram_bot_store7.telegram_bot import bot, send_order_notification  # Импортируем объект бота
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_order_notification_task(order_details):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Если цикл событий уже работает, используем run_coroutine_threadsafe
        asyncio.run_coroutine_threadsafe(send_order_notification(order_details), loop)
    else:
        # Если цикл событий не работает, запускаем его
        loop.run_until_complete(send_order_notification(order_details))


@shared_task
def send_order_confirmation_email(order_details, recipient_email):
    send_mail(
        subject='Подтверждение заказа',
        message=order_details,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
