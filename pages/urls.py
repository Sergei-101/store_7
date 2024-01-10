from django.urls import path
from pages.views import index, contact

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact')

]