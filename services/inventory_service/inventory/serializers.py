from rest_framework import serializers

from inventory.models import Product, StockMovement


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "sku",
            "name",
            "description",
            "price",
            "stock_quantity",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class StockMovementSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = StockMovement
        fields = ("id", "product", "product_sku", "movement_type", "quantity", "note", "created_at")
        read_only_fields = ("id", "created_at", "product_sku")


class StockAdjustSerializer(serializers.Serializer):
    quantity_delta = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)


class InternalConsumeItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class InternalConsumeSerializer(serializers.Serializer):
    items = InternalConsumeItemSerializer(many=True)
