from django.urls import path
from .views import (
    IndexView,
    ProductCreateView,
    ProductDeleteView,
    ProductListView,
    ProductRestoreView,
    ProductUpdateView,
    ProductVariantListView,
    ProductVariantCreateView,
    ProductVariantUpdateView,
    StockTransactionListView,
    StockTransactionCreateView
)

app_name = "dashboard"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/add", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/restore", ProductRestoreView.as_view(), name="product_restore"),

    # Variants
    path("variants/", ProductVariantListView.as_view(), name="variant_list"),
    path("variants/add/", ProductVariantCreateView.as_view(), name="variant_create"),
    path("variants/<int:pk>/edit/", ProductVariantUpdateView.as_view(), name="variant_update"),

    # Transactions
    # TODO: add transactions list section
    path("transactions/", StockTransactionListView.as_view(), name="transaction_list"),
    path("transactions/add/", StockTransactionCreateView.as_view(), name="transaction_create")
]
