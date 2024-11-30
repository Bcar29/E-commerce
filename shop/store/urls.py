from .views import *
from django.urls import path


urlpatterns = [
    path("" , home , name="home"),
    path("contact/" , contact , name="contact"),
    path("create/", Productcreate.as_view(), name="create"),
    path("listproduct/", ListProduct, name="listproduct"),
    path("detail/<int:pk>", ProductDetailView.as_view(), name="detail"),
    path("search/" , search , name="search"),
    path("detail/<int:pk>/add-to-cart" , add_to_cart , name="add-to-cart"),
    path("cart/" , cart , name="cart"),
    path("cart/delete" , cart_delete , name="cart-delete"),
    path("from-pai/" , form_pai , name="form-pai"),
    path("alivre/", OrderListView.as_view(), name="alivre"),
    path("<int:pk>/editorder" , OrderUpdateView.as_view() , name="editorder"),
    path('checkout/', checkout, name='checkout'),
    path('payment/execute/', execute_payment, name='execute_payment'),
    path("paiement" , paiement , name="paiement"),
    path("paiement/recu/<int:pk>" , recu , name="recu"),
    path("paiement/erecu/" , essairecu , name="erecu"),
    
]

