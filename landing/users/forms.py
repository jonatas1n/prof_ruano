from django import forms
from users.models import CustomUser


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirme a senha")
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")
        return email

    def save(self, commit=True):
        user = CustomUser()
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
