from django.urls import path
from users.views import login_register,registration

app_name = 'users'

urlpatterns = [
    path('login-register/', login_register, name='login_register'),


]