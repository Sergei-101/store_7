from django.urls import path
from baskets.views import basket_view

app_name = 'baskets'

urlpatterns = [

    path('basket_view/', basket_view, name='basket_view'),
]