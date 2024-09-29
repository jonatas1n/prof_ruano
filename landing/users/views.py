from django.shortcuts import render, redirect
from users.forms import RegisterForm
from django.views import View
from django.contrib import messages
from home.models import LandingPage


def login(request):
    return render(request, "users/login.html")


class UserRegistrationView(View):
    form_class = RegisterForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seu registro foi bem-sucedido!")
            return redirect("/")

        return render(request, self.template_name, {"form": form})
