from django.shortcuts import render, redirect
from users.forms import RegisterForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views import View


def login(request):
    return render(request, "users/login.html")
class UserRegistrationView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Seu registro foi bem-sucedido!")
            return redirect('/')

        return render(request, self.template_name, {'form': form})
