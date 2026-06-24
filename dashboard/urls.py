from django.urls import path
from .views import (
    IndexView,
    ProductCreateView,
    ProductListView,
    ProductVariantListView,
    ProductVariantCreateView,
    ProductVariantUpdateView,
    StockTransactionCreateView
)

app_name = "dashboard"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/add", ProductCreateView.as_view(), name="product_create"),

    # Variants
    path("variants/", ProductVariantListView.as_view(), name="variant_list"),
    path("variants/add/", ProductVariantCreateView.as_view(), name="variant_create"),
    path("variants/<int:pk>/edit/", ProductVariantUpdateView.as_view(), name="variant_update"),

    # Transactions
    # TODO: add transactions list section
    path("transactions/add/", StockTransactionCreateView.as_view(), name="transaction_create")
]
