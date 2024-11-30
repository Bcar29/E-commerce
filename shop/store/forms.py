from django import forms
from .models import Product, Order

class formProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "stock", "thumbnail", "categories", "description"]

    def __init__(self, *args, **kwargs):
        super(formProduct, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})
            self.fields[field].label = ''
            
class formOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user", "delivred"]

    def __init__(self, *args, **kwargs):
        super(formOrder, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
                