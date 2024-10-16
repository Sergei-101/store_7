# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_invoice_email(order_id, customer_email):
    from .models import Order  # Импортируем модель здесь, чтобы избежать циклических импортов
    
    order = Order.objects.get(id=order_id)
    subject = f'Ваш счет за заказ №{order.id}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [customer_email]
    
    html_message = render_to_string('invoice_email.html', {'order': order})
    
    send_mail(
        subject,
        '',
        from_email,
        to_email,
        html_message=html_message,
        fail_silently=False,
    )
