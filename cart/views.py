from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from products.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.http import JsonResponse
from django.core.serializers import serialize

def cart_add_quick(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return JsonResponse({'success': True, 'message': 'Товар успешно добавлен в корзину'})
    else:
        errors = form.errors.as_json()  # Получаем ошибки формы в JSON-формате
        return JsonResponse({'success': False, 'message': f'Произошла ошибка. Пожалуйста, проверьте введенные данные: {errors}'})


def get_cart_contents(request):
    cart = Cart(request)
    cart_items = []

    # Преобразуем каждый товар в корзине в словарь перед добавлением в список cart_items
    for item in cart:
        product_data = {
            'test':'test',
            'id': item['product'].id,
            'name': item['product'].name,
            'price': str(item['product'].final_price()),  # Получаем конечную цену товара
            'quantity': item['quantity'],
            'total_price': str(item['total_price']),
        }
        cart_items.append(product_data)

    total_price = str(cart.get_total_price())

    # Формируем JSON-объект с данными о содержимом корзины
    cart_contents = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return JsonResponse(cart_contents)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()
    contex = {'cart': cart,
              'coupon_apply_form': coupon_apply_form}
    return render(request, 'cart/detail.html', contex)
