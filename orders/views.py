from django.shortcuts import render

from orders.models import Order


def order_view(request):
    context = {
        'orders': Order.objects.filter(user=request.user)
    }
    return render(request, 'orders/order_view.html', context)

