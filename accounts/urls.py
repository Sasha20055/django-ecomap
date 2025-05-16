from django.urls import path
from .views import RegisterView, CustomLoginView, CustomPasswordResetView
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,  # добавили
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    CustomLoginView.as_view(), name='login'),
    path('logout/',   LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/',      CustomPasswordResetView.as_view(),  name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # новый маршрут для страницы после успешного сброса
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
