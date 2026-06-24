from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView
)

from .models import StockTransaction
from .forms import (
    Product,
    ProductForm,
    ProductVariant,
    ProductVariantForm,
    StockTransactionForm
)

class IndexView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        variants = ProductVariant.objects.all()

        context["total_variants"] = variants.count()
        context["low_stock_count"] = sum(
            1 for variant in variants if variant.is_low_stock
        )

        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    success_url = reverse_lazy("dashboard:variant_list")

    def form_valid(self, form):
        messages.success(self.request, "Product created successfully")
        return super().form_valid(form)

class ProductListView(ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return (Product.objects.order_by("name"))

class ProductVariantListView(ListView):
    model = ProductVariant
    template_name = "dashboard/productvariant_list.html"
    context_object_name = "variants"

    def get_queryset(self):
        return (
            ProductVariant.objects
            .select_related("product", "category")
            .order_by("product__name", "name")
        )

class ProductVariantCreateView(CreateView):
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = "dashboard/productvariant_form.html"
    success_url = reverse_lazy("dashboard:variant_list")

    def form_valid(self, form):
        messages.success(self.request, "Variant created successfully.")
        return super().form_valid(form)

class ProductVariantUpdateView(UpdateView):
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = "dashboard/productvariant_form.html"
    success_url = reverse_lazy("dashboard:variant_list")

    def form_valid(self, form):
        messages.success(self.request, "Variant updated successfully")
        return super().form_valid(form)

class StockTransactionCreateView(CreateView):
    model = StockTransaction
    form_class = StockTransactionForm
    template_name = "dashboard/stocktransaction_form.html"
    success_url = reverse_lazy("dashboard:variant_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(
                self.request,
                "Stock transaction recorded successfully."
            )
            return response

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
