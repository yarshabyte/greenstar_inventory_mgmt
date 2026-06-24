from django import forms
from .models import Product, ProductVariant, StockTransaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name"]

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = [
            "product",
            "name",
            "category",
            "description",
            "price",
            "color",
            "current_stock",
            "reorder_level",
        ]

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = [
            "variant",
            "transaction_type",
            "quantity",
            "notes"
        ]
