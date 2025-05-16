# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

rus_name_validator = RegexValidator(
    r'^[А-ЯЁ][а-яё]+$',
    "Должно быть на кириллице: первая буква заглавная, остальные строчные."
)
email_validator = RegexValidator(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
    "Неверный формат e‑mail."
)
password_validator = RegexValidator(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$',
    "Пароль ≥8 символов, с разным регистром, цифрами и спецсимволами."
)

class RegistrationForm(UserCreationForm):
    first_name  = forms.CharField(validators=[rus_name_validator])
    last_name   = forms.CharField(validators=[rus_name_validator])
    patronymic  = forms.CharField(validators=[rus_name_validator])
    email       = forms.EmailField(validators=[email_validator])
    password1   = forms.CharField(validators=[password_validator], widget=forms.PasswordInput)
    password2   = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','last_name','first_name','patronymic','email','password1','password2']