from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("logout/", logout_user, name="logout"),
    path("change/", password_change.as_view(), name="change"),
    path("password-reset/", password_reset.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>", password_reset_confirm.as_view(), name="password-reset-confirm"),
]