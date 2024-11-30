from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from shop.settings import AUTH_USER_MODEL

# Create your models here.

# ----------------------Categorie de produit---------------------------------#
class Categories(models.Model):
    name = models.CharField(max_length=128, )
    descriptions = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Categorie"

    def __str__(self) -> str:
        return self.name

# ---------------------------Produit (Product)---------------------------------#
class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name="nom du produit")
    # slug = models.SlugField(max_length=128, blank=True)
    price = models.FloatField(verbose_name="prix du produit")
    stock = models.IntegerField(verbose_name="Quantité stoker")
    thumbnail = models.ImageField(upload_to="products", blank=True, null= True)
    description = models.TextField(blank=True, verbose_name="Description du produit")
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Produit"
   

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk":self.pk})
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

# -----------------------Addresse de livraison-----------------------------------#
class ShippingAddress(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    pays = models.CharField(max_length=32)
    ville = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.pays} {self.ville} {self.zip_code}"
    

# ---------------------------Panier (cart)------------------------------------------#
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

# ---------------------------Article (Order)------------------------------------#
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderProduct") 
    shippingaddress = models.OneToOneField(ShippingAddress,null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="client", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1) 
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    montant = models.FloatField(default=0)
    delivred = models.CharField(max_length=50, choices=([
        ("En_attent","En attente"),
        ("En_cours", "En cours de traitement"),
        ("Annule", "Annulé"),
        ("Livrre", "Livrée")
    ]), default="En_attente", verbose_name="etat")
 
    def __str__(self):
        return f"{self.user} {self.quantity}"
    
    class Meta:
        verbose_name = "Commande"
        ordering = ["-quantity"]

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produits", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name="commande", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def tatol_amount(self):
        return self.quantity * self.product.price 
        
# -------------------------------Paiement------------------------------------------#
class Paiement(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    mount = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} {self.mount}" 
    def save(self, *args, **kwargs):
        cart = self.cart
        for order in cart.order_set.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.cart.order_set.clear()
        self.cart.order_set.all().delete()


        super().save(*args, **kwargs)



