import json
from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem
from orders.forms import PersonalOrderForm, BusinessOrderForm
from cart.cart import Cart
from products.models import Product
from django.shortcuts import render
from .forms import PersonalOrderForm, BusinessOrderForm
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required


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
            if cart.coupon:
                form.instance.total_cost = cart.get_total_price_after_discount()
            else:
                form.instance.total_cost = cart.get_total_price()               

            if request.user.is_authenticated:
                current_user = request.user
                form.instance.initiator = current_user
            if customer_type == 'business':
                form.instance.customer_type = 'business'
            else:
                form.instance.customer_type = 'personal'
            order = form.save()            
            for item in cart:
                product = get_object_or_404(Product, pk=item['product'].id)
                product.quantity -= item['quantity']
                if product.quantity <= 0:
                    product.available = False
                product.save()
                
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         total=item['price'] * item['quantity'])

            cart.clear()

            basket_history = OrderItem.objects.filter(order=order)
            return render(request, 'orders/complete.html', {'title': 'Оформление заказа','order': order, 'basket_history': basket_history, })

    return render(request, 'orders/create.html', {'title': 'Оформление заказа','cart': cart, 'personal_form': personal_form, 'business_form': business_form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})