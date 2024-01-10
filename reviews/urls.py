# reviews/urls.py
from django.urls import path
from .views import product_reviews, add_review

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
    path('product/<int:product_id>/add_review/', add_review, name='add_review'),
]
