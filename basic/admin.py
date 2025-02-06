from django.contrib import admin

# Register your models here.
from .models import Currency
from .models import QRCode
from .models import Product

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')
    search_fields = ('code', 'name')

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'generated_date', 'expiry_date', 'dynamic')
    search_fields = ('product_id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency', 'category', 'eco_friendly')
    search_fields = ('id', 'name', 'price', 'category', 'currency')