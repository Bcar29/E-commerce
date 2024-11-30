from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from shop import settings
from .forms import *
from django.contrib import messages

User = get_user_model()

# Create your views here.

# --------------------------------------------------------Inscription--------------------------------------------# 
def signup(request): 
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect("store:home")
        else:
            msg ="les deux password ne sont pas conforme"
            return render(request, "accounts/signup.html" , {'msg': msg})

    return render(request, "accounts/signup.html")

# --------------------------------------------------------Connexion-----------------------------------------------#
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("store:home")
        else:
            return redirect("signup")
        
    return render(request, "accounts/signin.html")

# ----------------------------------------------Deconnexion-----------------------------------------------------#
def logout_user(request):
    logout(request)
    return redirect("store:home")

# ------------------------------------------------changer le mot de passe ---------------------------------------#
class password_change(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    password_change_form = changeform
    success_url = reverse_lazy("store:home")

    def form_valid(self, form):
        messages.success(self.request, "Votre mot de passe a été changé avec succès.")
        return super().form_valid(form)

# -------------------------------------------------demande de reinitialisation de password-------------------------#
class password_reset(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    password_reset_form = resetform
    email_template_name = 'accounts/password_reset_email.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy("store:home")

    def form_valid(self, form):
        messages.info(self.request, "Verifiez votre boite email pour confirmez la reinitialisation.")
        return super().form_valid(form)

# ------------------------------------------------reinitialisation de password---------------------------------------#
class password_reset_confirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm_form.html'
    password_reset_form = resetconfirmform
    success_url = reverse_lazy("store:home")

    def form_valid(self, form):
        messages.success(self.request, "Votre mot de passe a été modifié avec succès.")
        return super().form_valid(form)
    