from django.shortcuts import render

from baskets.models import Basket


def basket_view(request):
    context = {
        'baskets': Basket.objects.filter(user=request.user)
    }
    return render(request, 'baskets/order_view.html', context)

