from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", "descriptions" )

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("user", "mount")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "thumbnail")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user", "quantity", "montant","ordered", "ordered_date", "delivred", )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", )

@admin.register(ShippingAddress)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "pays", "ville", "zip_code")