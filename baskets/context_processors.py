from baskets.models import Basket


def basket_view_cont_proc(request):
    if request.user.is_authenticated:
        return {'baskets': Basket.objects.filter(user=request.user)}
    else:
        return {'text': 'Корзина пуста'}


