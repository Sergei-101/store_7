from django.urls import path
from pages.views import index, static_page

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', static_page, name='static_page'),  # Путь для статических страниц

]