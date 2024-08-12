"""
URL configuration for store_7 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import index
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, ProductCategorySitemap, PostSitemap, CategorySitemap

sitemaps = {
    'products': ProductSitemap,
    'productcategories': ProductCategorySitemap,
    'post': PostSitemap,
    'category': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('cart/', include('cart.urls', namespace='cart')),    
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('__debug__/', include("debug_toolbar.urls")),



]

handler404 = 'pages.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)