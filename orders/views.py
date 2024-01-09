import json
from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if cart.coupon:
                form.instance.total_cost = cart.get_total_price_after_discount()
            else:
                form.instance.total_cost = cart.get_total_price()
            if request.user.is_authenticated:
                current_user = request.user
                form.instance.initiator = current_user

            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         total=item['price'] * item['quantity'])
            # очистить корзину
            basket_history = OrderItem.objects.filter(order=order)
            cart.clear()
            return render(request,'orders/complete.html',{'order': order,
                                                          'basket_history': basket_history,
                                                          })
    else:
        form = OrderCreateForm()
    return render(request,'orders/create.html',{'cart': cart, 'form': form})





