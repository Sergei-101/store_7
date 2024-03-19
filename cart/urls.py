from django.urls import path
from cart.views import cart_add, cart_detail, cart_remove, cart_add_quick, get_cart_contents

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('adds/<int:product_id>/', cart_add_quick, name='cart_add_quick'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('content/', get_cart_contents, name='get_cart_contents'),
]