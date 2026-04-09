from django.db import transaction
from django.db.models import F
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import Product, StockMovement
from inventory.permissions import HasInternalApiKey
from inventory.serializers import (
	InternalConsumeSerializer,
	ProductSerializer,
	StockAdjustSerializer,
	StockMovementSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	def get_permissions(self):
		if self.action in {"list", "retrieve"}:
			return [permissions.AllowAny()]
		return [permissions.IsAuthenticated()]

	@action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
	def adjust_stock(self, request, pk=None):
		product = self.get_object()
		serializer = StockAdjustSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		delta = serializer.validated_data["quantity_delta"]
		note = serializer.validated_data.get("note", "")
		new_stock = product.stock_quantity + delta
		if new_stock < 0:
			return Response({"detail": "Insufficient stock."}, status=status.HTTP_400_BAD_REQUEST)

		movement_type = (
			StockMovement.MOVEMENT_IN if delta > 0 else StockMovement.MOVEMENT_OUT if delta < 0 else StockMovement.MOVEMENT_ADJUST
		)
		product.stock_quantity = new_stock
		product.save(update_fields=["stock_quantity", "updated_at"])
		StockMovement.objects.create(
			product=product,
			movement_type=movement_type,
			quantity=delta,
			note=note,
		)
		return Response(ProductSerializer(product).data)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = StockMovement.objects.select_related("product")
	serializer_class = StockMovementSerializer
	permission_classes = [permissions.IsAuthenticated]


class InternalConsumeInventoryView(APIView):
	permission_classes = [HasInternalApiKey]

	def post(self, request):
		serializer = InternalConsumeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		items = serializer.validated_data["items"]

		with transaction.atomic():
			products = Product.objects.select_for_update().in_bulk([item["product_id"] for item in items])

			for item in items:
				product = products.get(item["product_id"])
				if not product:
					return Response({"detail": f"Product {item['product_id']} not found."}, status=status.HTTP_404_NOT_FOUND)
				if product.stock_quantity < item["quantity"]:
					return Response(
						{"detail": f"Insufficient stock for product {product.id}."},
						status=status.HTTP_400_BAD_REQUEST,
					)

			for item in items:
				product = products[item["product_id"]]
				Product.objects.filter(id=product.id).update(stock_quantity=F("stock_quantity") - item["quantity"])
				StockMovement.objects.create(
					product=product,
					movement_type=StockMovement.MOVEMENT_OUT,
					quantity=-item["quantity"],
					note="Consumed by order-service checkout",
				)

		return Response({"detail": "Stock consumed successfully."}, status=status.HTTP_200_OK)
