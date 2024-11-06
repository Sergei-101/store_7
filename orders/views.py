import asyncio
import json
from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem
from orders.forms import PersonalOrderForm, BusinessOrderForm
from cart.cart import Cart
from products.models import Product
from django.shortcuts import render
from orders.tasks import send_order_notification_task, send_order_confirmation_email
from parser_store.views import update_price
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
            basket_history = OrderItem.objects.filter(order=order)
            # Отправляем уведомление о заказе асинхронно
            # send_order_notification_task.delay(order_details)
            # Отправляем подтверждение заказа по электронной почте
            # email = request.user.email if request.user.is_authenticated else form.cleaned_data['email']
            # send_order_confirmation_email.delay(order_details, email)

            return render(request, 'orders/complete.html', {'title': 'Оформление заказа', 'order': order, 'basket_history': basket_history})

    return render(request, 'orders/create.html', {'title': 'Оформление заказа', 'cart': cart, 'personal_form': personal_form, 'business_form': business_form})




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

@staff_member_required
def check_prices(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    price_checks = []
    total_difference = 0
    total_profit = 0

    # Проверяем цены для каждого товара в заказе
    for item in order.items.all():
        price_data = update_price(item.product.id)

        if price_data:
            try:
                # Получаем текущую цену (цена на сайте) и новую цену (цена поставщика)
                current_cost = float(price_data.get('current_price', 0))
                new_cost = price_data.get('new_price', "N/A")

                if new_cost == "N/A" or new_cost == 0:
                    # Если новая цена недоступна
                    new_cost = "Не учитывается"
                    price_difference = "Не учитывается"
                    potential_profit = "Не учитывается"
                else:
                    # Если новая цена есть, вычисляем разницу в цене и прибыль
                    new_cost = float(new_cost)
                    price_difference = round((current_cost - new_cost) * item.quantity, 2)
                    potential_profit = round((current_cost - new_cost) * item.quantity, 2)

                    # Обновляем общую разницу и прибыль
                    total_difference += price_difference
                    total_profit += potential_profit

                price_checks.append({
                    'name': price_data.get('name', 'Неизвестно'),
                    'current_cost': round(current_cost, 2),
                    'new_cost': new_cost,
                    'unit': price_data.get('unit', 'Неизвестно'),
                    'quantity': item.quantity,
                    'price_difference': price_difference,
                    'potential_profit': potential_profit,
                    'status': 'Цена изменилась' if current_cost != new_cost else 'Цена актуальна'
                })
            except ValueError as e:
                # Обработка ошибки преобразования типа
                price_checks.append({
                    'name': item.product.name,
                    'current_cost': 'Ошибка',
                    'new_cost': 'Ошибка',
                    'unit': 'Неизвестно',
                    'quantity': item.quantity,
                    'price_difference': 'Ошибка',
                    'potential_profit': 'Ошибка',
                    'status': f'Ошибка преобразования данных: {e}'
                })
        else:
            # Обработка случая, когда данные цены отсутствуют
            price_checks.append({
                'name': item.product.name,
                'current_cost': 'Неизвестно',
                'new_cost': 'Неизвестно',
                'unit': 'Неизвестно',
                'quantity': item.quantity,
                'price_difference': 'Ошибка',
                'potential_profit': 'Ошибка',
                'status': 'Ошибка при обновлении цены'
            })

    # Рендеринг шаблона с результатами проверки цен
    return render(request, 'admin/orders/order/check_prices.html', {
        'price_checks': price_checks,
        'order': order,
        'total_difference': round(total_difference, 2),
        'total_profit': round(total_profit, 2)
    })



def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Отправитель
        recipient_list,  # Список получателей
        fail_silently=False,
    )