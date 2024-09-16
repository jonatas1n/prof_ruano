from django.shortcuts import render, redirect
from users.models import CustomUser
from users.forms import RegisterForm

def login(request):
    return render(request, 'users/login.html')

def register(request):
    if request.user.is_authenticated:
        redirect("/auth")

    form = RegisterForm()
    if request.method == "POST":
        form.data = request.POST
        if form.is_valid():
            form.save()
            return redirect("/auth")
        return render(request, "users/register.html", {"form": form, "error": form.errors})
    

    return render(request, "users/register.html", {"success": True, "form": form})