from django.urls import path
from users.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    # path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/reset.html", success_url="/"
        ),
        name="password_reset_confirm",
    ),
]
