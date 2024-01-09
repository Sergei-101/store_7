from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm

def login_register(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        form_2 = UserRegisterForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        if form_2.is_valid():
            form_2.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
        form_2 = UserRegisterForm()
    context = {'form': form,
               'form_2': form_2}
    return render(request, 'users/login_register.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Profile in store',
               'form': form,
               }
    return render(request, 'users/profile.html', context)


def profile_orders(request):
    orders = Order.objects.filter(initiator=request.user)
    context = {'orders': orders}
    return render(request, 'users/profile_orders.html',context)
def profile_order_detail(request, order_id):
    order = Order.objects.filter(id=order_id)
    order_item = OrderItem.objects.filter(order=order_id)
    context = {'orders':order, 'order_items': order_item}
    return render(request, 'users/profile_orders_detail.html', context)

def profile_wishlist(request):
    return render(request, 'users/profile_wishlist.html')









