from django.shortcuts import render

# Create your views here
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from .forms import (
    LoginForm,
    UserCreationForm
)

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class LogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = '/accounts/login/'
    template_name = 'accounts/signup.html'

