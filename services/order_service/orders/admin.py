from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "user_id", "status", "total_amount", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("id", "user_id")
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("id", "order", "product_id", "product_name", "quantity", "line_total")
	search_fields = ("product_name", "product_id")
