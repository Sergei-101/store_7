from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.forms import UserLoginForm, UserRegisterForm

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





