from django.urls import path
from users.views import login_register, profile, profile_orders, profile_address, profile_wishlist, logout

app_name = 'users'

urlpatterns = [
    path('login-register/', login_register, name='login_register'),
    path('profile/', profile, name='profile'),
    path('profile-orders/', profile_orders, name='profile_orders'),
    path('profile-address/', profile_address, name='profile_address'),
    path('profile-wishlist/', profile_wishlist, name='profile_wishlist'),
    path('logout/', logout, name='logout'),
]