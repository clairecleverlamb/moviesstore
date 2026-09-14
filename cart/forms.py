from django import forms
from django.forms import inlineformset_factory

from .models import Item, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['movie', 'quantity', 'price']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def clean(self):
        cleaned = super().clean()
        movie = cleaned.get('movie')
        if movie and cleaned.get('price') in (None, ''):
            cleaned['price'] = movie.price
        return cleaned


ItemFormSet = inlineformset_factory(
    Order,
    Item,
    form=ItemForm,
    extra=1,
    can_delete=True,
)
