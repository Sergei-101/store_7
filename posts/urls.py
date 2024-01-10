from django.urls import path
from posts.views import all_post, post_category,post_detail

app_name = 'posts'

urlpatterns = [
    path('', all_post, name='index'),
    path('category/<int:category_id>', post_category, name='post_category'),
    path('detail/<int:post_id>', post_detail, name='post_detail'),

]