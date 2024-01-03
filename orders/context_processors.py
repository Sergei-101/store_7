from orders.models import Order


def order_view_cont_proc(request):
    if request.user.is_authenticated:
        return {'orders': Order.objects.filter(user=request.user)}
    else:
        return {'text': 'Корзина пуста'}


