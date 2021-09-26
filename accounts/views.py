from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'accounts/register.html'

class SentView(TemplateView):
    template_name = 'accounts/sent.html'

# Create your views here.
