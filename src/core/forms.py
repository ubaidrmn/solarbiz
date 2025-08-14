from django import forms
from core import models


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = [
            'name',
            'phone',
            'city',
            'address',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+92-3xx-xxxxxxx'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Street, Area, City', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Any additional notes', 'rows': 3}),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['description', 'unit_price', 'warranty_years', 'product_type', 'brand', 'cost_price', 'rating_kw']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter default price'}),
            'warranty_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter warranty years'}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter cost price'}),
            'rating_kw': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter rating in KW'}),
        }
