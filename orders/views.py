from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.initiator = current_user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистить корзину
            cart.clear()
            return render(request,'orders/complete.html',{'order': order})
    else:
        form = OrderCreateForm()
    return render(request,'orders/test.html',{'cart': cart, 'form': form})





