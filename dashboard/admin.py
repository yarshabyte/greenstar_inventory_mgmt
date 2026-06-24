from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Category, Product, ProductVariant, StockTransaction

# TODO: add meaningful comments :)
# Custom Filter
class SoftDeleteFilter(SimpleListFilter):
    title = 'Deletion Status'
    parameter_name = 'deleted_status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active Only'),
            ('deleted', 'Deleted Only'),
            ('all', 'All Records'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'deleted':
            return queryset.filter(is_deleted=True)
        elif self.value() == 'active':
            return queryset.filter(is_deleted=False)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'description')
    ordering = ('name',)

    def get_queryset(self, request):
        return self.model.all_objects.all()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted', 'created_at')
    list_filter = (SoftDeleteFilter,)
    search_fields = ('name',)

    def get_queryset(self, request):
        return self.model.all_objects.all()


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'name', 'sku', 'category', 'price',
        'current_stock', 'reorder_level', 'is_low_stock', 'is_deleted'
    )
    list_filter = ('category', SoftDeleteFilter, 'product')
    search_fields = ('name', 'sku', 'product__name')
    list_editable = ('price', 'current_stock', 'reorder_level')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('product', 'name', 'sku', 'category', 'description', 'price', 'color')
        }),
        ('Stock', {
            'fields': ('current_stock', 'reorder_level')
        }),
        ('System Fields', {
            'fields': ('is_deleted', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return self.model.all_objects.all()


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'variant', 'transaction_type', 'quantity',
        'transaction_date', 'notes'
    )
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('variant__name', 'variant__sku', 'notes')
    readonly_fields = ('transaction_date',)
    ordering = ('-transaction_date',)

    fieldsets = (
        (None, {
            'fields': ('variant', 'transaction_type', 'quantity', 'notes')
        }),
        ('Date', {
            'fields': ('transaction_date',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
