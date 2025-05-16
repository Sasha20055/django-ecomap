from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # у AbstractUser уже есть username, email, password, first_name, last_name
    patronymic = models.CharField("Отчество", max_length=150)

    ROLE_CHOICES = [
        ('ADMIN', 'Администратор'),
        ('USER', 'Пользователь'),
    ]
    role = models.CharField("Роль", max_length=5, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_role_display()})"