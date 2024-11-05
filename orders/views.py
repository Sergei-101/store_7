import asyncio
import json
from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem
from orders.forms import PersonalOrderForm, BusinessOrderForm
from cart.cart import Cart
from products.models import Product
from django.shortcuts import render
from orders.tasks import send_order_notification_task, send_order_confirmation_email
from telegram_bot_store7.telegram_bot import send_order_notification
from .forms import PersonalOrderForm, BusinessOrderForm
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
import threading
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.conf import settings
 # Импортируйте функцию отправки уведомлений

def order_create(request):
    cart = Cart(request)
    personal_form = PersonalOrderForm()
    business_form = BusinessOrderForm()

    if request.method == 'POST':
        customer_type = request.POST.get('customer_type')
        if customer_type == 'business':
            form = BusinessOrderForm(request.POST)
        else:
            form = PersonalOrderForm(request.POST)

        if form.is_valid():
            # Рассчитываем итоговую стоимость
            if cart.coupon:
                form.instance.total_cost = cart.get_total_price_after_discount()
            else:
                form.instance.total_cost = cart.get_total_price()

            # Присваиваем инициатора заказа, если пользователь авторизован
            if request.user.is_authenticated:
                form.instance.initiator = request.user

            form.instance.customer_type = customer_type
            order = form.save()

            # Формируем детали заказа для отправки
            order_details = f"Заказ ID: {order.id}\n"
            order_details += f"Клиент: {request.user.username if request.user.is_authenticated else 'Гость'}\n"
            order_details += f"Тип клиента: {customer_type.capitalize()}\n"
            order_details += "Товары:\n"

            for item in cart:
                product = get_object_or_404(Product, pk=item['product'].id)
                product.quantity -= item['quantity']
                if product.quantity <= 0:
                    product.available = False
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    total=item['price'] * item['quantity']
                )

                order_details += f"- {item['product'].name} (кол-во: {item['quantity']}, цена: {item['price']})\n"

            cart.clear()

            # Отправляем уведомление о заказе асинхронно
            send_order_notification_task.delay(order_details)
            # Отправляем подтверждение заказа по электронной почте
            email = request.user.email if request.user.is_authenticated else form.cleaned_data['email']
            send_order_confirmation_email.delay(order_details, email)

            return render(request, 'orders/complete.html', {'title': 'Оформление заказа', 'order': order})

    return render(request, 'orders/create.html', {'title': 'Оформление заказа', 'cart': cart, 'personal_form': personal_form, 'business_form': business_form})




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Отправитель
        recipient_list,  # Список получателей
        fail_silently=False,
    )