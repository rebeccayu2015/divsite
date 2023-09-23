from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Signed up successfully.")
            return redirect('home_page')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/sign_up.html', context)


class MyLoginView(SuccessMessageMixin, LoginView):    
    template_name = 'registration/login.html'
    success_url = ''
    # success_message = "Logged in successfully."
    


def logout(request):
    auth_logout(request)
    # messages.success(request, "Logged out successfully.")
    return redirect('login')
