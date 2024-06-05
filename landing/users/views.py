from django.shortcuts import render, redirect
from users.models import CustomUser

def login(request):
    return render(request, 'users/login.html')

def register(request):
    if request.user.is_authenticated:
        redirect("/auth")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        user = CustomUser.objects.filter(email=email)
        if user:
            return render(
                request, "users/register.html", {"error": "Usuário já cadastrado"}
            )

        if password != confirm_password:
            return render(
                request, "users/register.html", {"error": "Senhas não conferem"}
            )

        try:
            CustomUser.objects.create_user(email, password)
        except Exception as e:
            return render(request, "users/register.html", {"error": e})

        return redirect("/auth")

    return render(request, "users/register.html", {"success": True})