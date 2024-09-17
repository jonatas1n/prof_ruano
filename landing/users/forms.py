from django import forms
from users.models import CustomUser


class RegisterForm(forms.Form):
    class meta:
        model = CustomUser
        fields = ["email", "password", "confirm_password"]

    email = forms.EmailField(label="Email", max_length=255)
    password = forms.CharField(
        label="Senha", max_length=255, widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label="Confirme a senha", max_length=255, widget=forms.PasswordInput
    )

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        user = CustomUser.objects.filter(email=email)
        if user:
            raise Exception("Usuário já cadastrado")

        if password != confirm_password:
            raise Exception("Senhas não conferem")

        CustomUser.objects.create_user(email, password)
        return True
