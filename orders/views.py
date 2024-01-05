from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from baskets.models import Basket
from orders.forms import OrderCreateForm
from orders.models import OrderItem

def order_create(request):
    baskets = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for basket in baskets:
                OrderItem.objects.create(order=order,
                                         product=basket.product,
                                         quantity=basket.quantity,
                                         price=basket.product.price)
            baskets.clear()
            return render(request, 'products/products.html', {'order': order})
    else:
        form = OrderCreateForm()
    context = {'form': form, 'baskets':baskets}
    return render(request, 'orders/create.html', context)



