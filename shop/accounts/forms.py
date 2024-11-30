from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

class changeform(PasswordChangeForm):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirmer le nouveau", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    def __init__(self, *args, **kwargs):
        super(changeform, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            


class resetform(PasswordResetForm):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"placeholder": "entrer votre addresse email"}) )


class resetconfirmform(SetPasswordForm):
    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirmer le nouveau", widget=forms.PasswordInput(attrs={"class": "form-control"}))


