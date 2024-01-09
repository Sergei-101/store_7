from django.urls import path
from users.views import login_register, profile, profile_orders, profile_order_detail, profile_wishlist, logout

app_name = 'users'

urlpatterns = [
    path('login-register/', login_register, name='login_register'),
    path('profile/', profile, name='profile'),
    path('profile-orders/', profile_orders, name='profile_orders'),
    path('profile-orders-detail/<int:order_id>', profile_order_detail, name='profile_order_detail'),
    path('profile-wishlist/', profile_wishlist, name='profile_wishlist'),
    path('logout/', logout, name='logout'),
]