import asyncio
from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram_bot import send_order_notification

@receiver(post_save, sender=Order)
def send_telegram_notification(sender, instance, created, **kwargs):
    if created:
        order_details = f"Заказ #{instance.id}:\n"  # Соберите нужные детали заказа
        asyncio.run(send_order_notification(order_details))
