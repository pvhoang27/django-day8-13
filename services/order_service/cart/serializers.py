from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_id",
            "product_name",
            "unit_price",
            "quantity",
            "line_total",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "line_total", "created_at", "updated_at")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user_id", "items", "created_at", "updated_at")
        read_only_fields = fields
