import asyncio
from decimal import Decimal
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
from .models import OrderItem, Order, StoreDetails
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
            store_detail = StoreDetails.objects.first()
            if store_detail:
                form.instance.store_details = store_detail
            else:
                # Обработайте случай, когда нет данных в StoreDetails, например:
                raise ValueError("Нет доступных записей в StoreDetails.")
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
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                    total=item['price'] * item['quantity'],
                    product_data = {
                        "name": product.name,
                        "quantity": product.quantity,
                        "unit": product.unit.name if product.unit else "Unknown",
                        "base_price": float(product.base_price) if isinstance(product.base_price, Decimal) else product.base_price,
                        "markup_percentage": float(product.markup_percentage) if isinstance(product.markup_percentage, Decimal) else product.markup_percentage,
                        "vat_price": float(product.vat_price) if isinstance(product.vat_price, Decimal) else product.vat_price,
                        "manufacturer": product.manufacturer.name if product.manufacturer else None,
                        "supplier": product.supplier.supplier if product.supplier else None,
                        "promotion": product.promotion.name if product.promotion else None,
                        "what_shop": {
                            "shop_in_VAT": {
                                "name": product.name,
                                "base_price": float(product.price_with_markup()) if isinstance(product.price_with_markup(), (float, Decimal)) else float(product.price_with_markup()),
                                "unit": str(product.unit.name) if product.unit else "Unknown",
                                "quantity": item['quantity'],
                                "total": round(float(product.price_with_markup()) * item['quantity'], 2) if isinstance(product.price_with_markup(), (float, Decimal)) else round(product.price_with_markup() * item['quantity'], 2),
                                "vat_price": float(product.vat_price) if isinstance(product.vat_price, Decimal) else product.vat_price,
                                "vat_in_price": 0 if product.vat_price == 0 else round((float(product.price_with_markup()) * item['quantity']) * 20 / 100, 2) if isinstance(product.price_with_markup(), Decimal) else round((product.price_with_markup() * item['quantity']) * 20 / 120, 2),
                                "sum_in_vat": float(product.final_price()) * item['quantity'] if isinstance(product.final_price(), (float, Decimal)) else float(product.final_price()) * item['quantity'],
                            },
                            "shop_not_VAT": {
                                "name": product.name,
                                "base_price": float(product.final_price()) if isinstance(product.final_price(), (float, Decimal)) else float(product.final_price()),
                                "unit": str(product.unit.name) if product.unit else "Unknown",
                                "quantity": item['quantity'],
                                "total": round(float(product.final_price()) * item['quantity'], 2) if isinstance(product.final_price(), Decimal) else round(product.final_price() * item['quantity'], 2),
                                "vat_price": "без НДС",
                                "vat_in_price": 0,
                                "sum_in_vat": float(product.final_price()) * item['quantity'] if isinstance(product.final_price(), (float, Decimal)) else float(product.final_price()) * item['quantity'],
                            }
                        }
                    }

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
    seller_details = StoreDetails.objects.first()  # Получаем реквизиты магазина
    shop_in_vat = seller_details.is_nds # Проверяем, работает ли магазин с НДС
    total_summ_not_vat = 0
    total_vat = 0
    total_sum_in_vat = 0
    for item in order.items.all():
        product_data = item.product_data
        if shop_in_vat:
            shop_vat_data = product_data.get("what_shop", {}).get("shop_in_VAT", {})
            total_summ_not_vat += shop_vat_data.get("total", 0)
            total_vat += shop_vat_data.get("vat_in_price", 0)
            total_sum_in_vat += shop_vat_data.get("sum_in_vat", 0)
        else:
            shop_vat_datas = product_data.get("what_shop", {}).get("shop_not_VAT", {})
            total_summ_not_vat += shop_vat_datas.get("total", 0)            
            total_sum_in_vat += shop_vat_datas.get("sum_in_vat", 0)

    
    return render(request, 'admin/orders/order/invoice.html', {
        'order': order,
        'seller_details': seller_details,
        'shop_in_vat': shop_in_vat,
        'total_summ_not_vat': round(total_summ_not_vat,2),
        'total_vat': round(total_vat,2),
        'total_sum_in_vat': round(total_sum_in_vat,2),
        
        
    })



@staff_member_required
def check_prices(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    price_checks = []    
    total_sebestoimost = 0 
    total_in_chet = 0
    difference_supplier_and_site = None

    # Проверяем цены для каждого товара в заказе
    for item in order.items.all():
        price_data = update_price(item.product.id)

        if price_data:
            try:
                current_cost = float(price_data.get('current_price', 0))
                new_cost = price_data.get('new_price', None)
                markup_percentage = float(price_data.get('markup_percentage', 0))
                supplier = price_data.get('supplier', None)
                product_link = price_data.get('product_link', None)
                
                # Если нет цены от поставщика, рассчитываем потенциальную прибыль
                if new_cost == "N/A" or new_cost == 0:
                    price_difference_sebest = round((current_cost-(current_cost * (markup_percentage / 100))) * item.quantity, 2)  
                    difference_supplier_and_site = 0
                    
                else:
                    new_cost = float(new_cost)                    
                    price_difference_sebest = round(new_cost  * item.quantity, 2)   
                    difference_supplier_and_site = round((100 - ((new_cost * 100) / current_cost)),2)
                                   
                total_sebestoimost += price_difference_sebest                    
                total_in_chet += round(current_cost * item.quantity, 2)
                
                price_checks.append({
                    'name': price_data.get('name', 'Неизвестно'),
                    'current_cost': round(current_cost, 2),
                    'new_cost': new_cost if new_cost != "N/A" else "Не учитывается",
                    'unit': price_data.get('unit', 'Неизвестно'),
                    'quantity': item.quantity,
                    'difference_supplier_and_site':difference_supplier_and_site if difference_supplier_and_site else "N/A",
                    'supplier':supplier,
                    'product_link': product_link,
                    'status': 'Актуальна' if current_cost != new_cost else 'Изменилась'
                })
            except ValueError as e:
                price_checks.append({
                    'name': item.product.name,
                    'current_cost': 'Ошибка',
                    'new_cost': 'Ошибка',
                    'unit': 'Неизвестно',
                    'quantity': item.quantity,
                    'price_difference': 'Ошибка',
                    'potential_difference': 'Ошибка',
                    'status': f'Ошибка преобразования данных: {e}'
                })
        else:
            price_checks.append({
                'name': item.product.name,
                'current_cost': 'Неизвестно',
                'new_cost': 'Неизвестно',
                'unit': 'Неизвестно',
                'quantity': item.quantity,
                'price_difference': 'Ошибка',
                'potential_difference': 'Ошибка',
                'status': 'Ошибка при обновлении цены'
            })

    return render(request, 'admin/orders/order/check_prices.html', {
        'price_checks': price_checks,
        'order': order,
        'total_sebestoimost': round(total_sebestoimost, 2),
        'total_pribil': round(total_in_chet - total_sebestoimost, 2),
        'total_in_chet': round(total_in_chet, 2),
        'supplier':supplier

    })




def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Отправитель
        recipient_list,  # Список получателей
        fail_silently=False,
    )