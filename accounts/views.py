# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from .forms import RegistrationForm

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

# PasswordResetDoneView и PasswordResetConfirmView можно подключить с дефолтными шаблонами