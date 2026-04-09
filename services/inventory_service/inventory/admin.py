from django.contrib import admin

from inventory.models import Product, StockMovement


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id", "sku", "name", "price", "stock_quantity", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("sku", "name")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
	list_display = ("id", "product", "movement_type", "quantity", "created_at")
	list_filter = ("movement_type", "created_at")
	search_fields = ("product__sku", "product__name", "note")
