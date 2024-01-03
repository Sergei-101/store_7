from users.forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse


def log_reg_form(request):
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

    return {'form': form, 'form_2': form_2}
