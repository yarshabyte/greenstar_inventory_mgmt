from django.contrib import messages
from django.db.models import Q, Count, QuerySet
from django.http import request
from django.shortcuts import _get_queryset, render, redirect
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

# helper search
class Search:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get("q")

        if query:
            q_object = Q()

            for field in self.search_fields:
                q_object |= Q(**{f"{field}__icontains": query})

            queryset = queryset.filter(q_object)

        return queryset

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    success_url = reverse_lazy("dashboard:variant_list")

    def form_valid(self, form):
        messages.success(self.request, "Product created successfully")
        return super().form_valid(form)

class ProductListView(Search, ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"
    search_fields = ["name"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(variant_count=Count("variants"))
            .order_by("name")
        )

class ProductVariantListView(Search, ListView):
    model = ProductVariant
    template_name = "dashboard/productvariant_list.html"
    context_object_name = "variants"
    search_fields = ["name", "sku", "product__name"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
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
