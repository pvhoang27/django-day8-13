from django.contrib import admin

from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ("id", "user_id", "updated_at")
	search_fields = ("user_id",)
	inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ("id", "cart", "product_id", "product_name", "quantity", "updated_at")
	search_fields = ("product_name", "product_id")
