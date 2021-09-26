from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
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

    '''
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if username not in User.objects.username:
            User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                )
        return redirect(self.success_url)
    '''

# Create your views here.
