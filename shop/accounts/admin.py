from django.contrib import admin
from .models import Shopper
# Register your models here.
@admin.register(Shopper)
class ShopperAdmin(admin.ModelAdmin):
    list_display = ("username", "email")