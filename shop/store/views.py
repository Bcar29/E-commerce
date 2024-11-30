from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from store.forms import formProduct, formOrder
from .models import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from shop import settings
from weasyprint import CSS, HTML
from django.template.loader import render_to_string

import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# Create your views here.
# --------------------------------------------------LA PAGE D'ACCUEIL---------------------------------------------------------------------#
def home(request):
    product = Product.objects.all()[:5]
    return render(request, "store/index.html", context={"product":product})

# ---------------------------------------------PAGE D'ERREUR PERSONNALISER----------------------------------------------------------------#
def handle404(request, exception):
    return render(request, 'store/pages-error-404.html', status=404)

# ------------------------------------------------------------CONTACT---------------------------------------------------------------------#
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        send_mail(
                subject = f"{name} vous a contacter pour le sujet : {sujet}",
                message = message,
                from_email = email,
                recipient_list = [settings.EMAIL_HOST_USER],
                fail_silently=False,
        )
    return render(request, 'store/contact.html')


# -------------------------------------------------AJOUTER UN PRODUIT---------------------------------------------------------------------#
class Productcreate(UserPassesTestMixin,CreateView):
    model = Product
    form_class = formProduct
    def test_func(self) -> bool | None:
        return self.request.user.is_superuser
     
    def handle_no_permission(self): 
        return HttpResponseForbidden("vous n'êtes pas autorisez à naviguer ici")
    success_url = reverse_lazy("store:home")

#-------------------------------------------LISTE DES PRODUITS----------------------------------------------------------------------------#
def  ListProduct(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    try: 
        prods = paginator.page(page)
    except PageNotAnInteger:
        prods = paginator.page(1)
    except EmptyPage :
        prods = paginator.page(paginator.num_pages)
    return render(request, 'store/product_list.html', {"products": prods})


# ------------------------------------------------LES DETAILS D'UN PRODUIT----------------------------------------------------------------#
class ProductDetailView(DetailView):
    model = Product
    template_name = "store/detail.html"

    
# -----------------------------------------------RECHERCHER UN PRODUIT--------------------------------------------------------------------#
def search(request):
    product = None
    if query := request.GET.get('query'):
        product = Product.objects.filter(name__icontains = query)
        return render(request, 'store/search.html', {'product':product, 'query':query})
    return render(request, 'store/index.html')


# --------------------------------------------AJOUT DE PRODUIT DANS LE PANIER-------------------------------------------------------------#
def add_to_cart(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, _ = Order.objects.get_or_create(user=user, ordered=False)

    order.cart = cart
    # Vérifie si le produit est déjà dans la commande
    order_product, created_order_product = OrderProduct.objects.get_or_create(order=order, product=product)

    if created_order_product:
        order_product.quantity = 1  
    else:
        order_product.quantity += 1

    order_product.save() 

    # Calculer le montant total de la commande
    order.montant = sum(op.tatol_amount() for op in order.orderproduct_set.all())
    order.save()
    
    return redirect('store:home')

# -------------------------------------------------LE CONTENU DU PANIER-------------------------------------------------------------------#
def cart(request):
    order = get_object_or_404(Order, user = request.user, ordered = False)
    order_products = order.orderproduct_set.all()
    return render(request, "store/cart.html", {"orders": order, "order_products": order_products, "montant": order.montant})


# -----------------------------------------------VIDER LE PANIER--------------------------------------------------------------------------#
def cart_delete(request):
    cart = Cart.objects.get(user = request.user)
    cart.order_set.all().filter(user = request.user, ordered = False).delete()
    return redirect("store:home")

# ---------------------------------------------PAGE DE PAIEMENT---------------------------------------------------------------------------#
def form_pai(request):
    order = get_object_or_404(Order, user = request.user, ordered = False)
    return render(request, 'store/form_pai.html', {'montant': order.montant})


# -----------------------------------------------RECU DE PAIMENT--------------------------------------------------------------------------#
def recu(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_products = order.orderproduct_set.all()
    html_string = render_to_string('store/recu.html', {"order_products": order_products, "Order": order, })
    # css_files = [
    #              CSS(settings.STATIC_URL + 'store/css/all.min.css'),
    #              CSS(settings.STATIC_URL + 'store/css/bootstrap.min.css'),
    #              CSS(settings.STATIC_URL + 'store/css/recu.css'),]
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachement; filename="recu_{order.pk}.pdf"'
    return response
      



def paiement(request):
    # recuperation de l'addresse de livraison 
    if request.method == 'POST':
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        zip = request.POST.get('zip')
        ShippingAddress.objects.create(user = request.user, pays = pays, ville = ville, zip_code = zip)

    # l'attribution de l'addrese à la commnde
    addrese = ShippingAddress.objects.filter(user=request.user).last()
    if addrese is not None:
        order = Order.objects.get(user=request.user, ordered=False)
        order.shippingaddress = addrese
        order.save() 

    # recuperation des donnees du payement 
    order = get_object_or_404(Order, user = request.user, ordered = False)
    cart = get_object_or_404(Cart, user = request.user)
    if request.method == 'POST':
        tel = request.POST.get('tel')
        Paiement.objects.create(user = request.user, cart = cart, mount = order.montant)
        return redirect('store:home')

    return render(request, 'store/form_pai.html')

# ----------------------------------------------COMMANDE A LIVREE-------------------------------------------------------------------------#
class OrderListView(ListView):
    queryset = Order.objects.filter(delivred = "En_attente")
    template_name = "store/commandealivre.html"
     
# -------------------------------------------METTRE A JOUR UNE COMMANDE-------------------------------------------------------------------#
class OrderUpdateView(UpdateView):
    model = Order
    template_name = "store/commandeupdate.html"
    form_class = formOrder
    success_url = reverse_lazy("store:alivre")

# ----------------------------------------SYSTEME DE PAIEMENT AVEC PAYPAL-----------------------------------------------------------------#
def checkout(request):
    order = get_object_or_404(Order, user = request.user, ordered = False)
    order.montant = order.quantity * sum(product.price for product in order.products.all())

    if request.method == "POST":
        # Créer un objet de paiement
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/store/payment/execute/",
                "cancel_url": "http://localhost:8000/store/"
            },
            "transactions": [{
                "amount": {
                    "total": order.montant,
                    "currency": "USD"
                },
                "description": "la transaction vers le site Alfa"
            }]
        })

        # Créer le paiement
        if payment.create():
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            print(payment.error)

    return render(request, 'checkout.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return HttpResponse("Payment executed successfully")
    else:
        return HttpResponse("Payment execution failed")



def essairecu(request):
    order = get_object_or_404(Order, pk=39)
    order_products = order.orderproduct_set.all()
    return render(request, 'store/recu.html', {"order_products": order_products, "Order": order })