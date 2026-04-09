from decimal import Decimal

import requests
from django.conf import settings
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


def _get_user_id(request) -> int:
	return int(request.user.id)


class OrderListView(generics.ListAPIView):
	serializer_class = OrderSerializer

	def get_queryset(self):
		user_id = _get_user_id(self.request)
		return Order.objects.filter(user_id=user_id).prefetch_related("items")


class CheckoutView(APIView):
	def post(self, request):
		user_id = _get_user_id(request)
		cart = Cart.objects.prefetch_related("items").filter(user_id=user_id).first()
		if not cart or not cart.items.exists():
			return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

		items_payload = [{"product_id": item.product_id, "quantity": item.quantity} for item in cart.items.all()]

		consume_url = f"{settings.ORDER_INVENTORY_BASE_URL}/api/v1/inventory/internal/consume/"
		try:
			response = requests.post(
				consume_url,
				json={"items": items_payload},
				headers={"X-INTERNAL-API-KEY": settings.ORDER_INVENTORY_INTERNAL_API_KEY},
				timeout=5,
			)
			response.raise_for_status()
		except requests.RequestException as exc:
			return Response(
				{"detail": f"Inventory service error: {exc}"},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		with transaction.atomic():
			order = Order.objects.create(user_id=user_id, status=Order.STATUS_CONFIRMED)
			total_amount = Decimal("0")

			for cart_item in cart.items.all():
				line_total = cart_item.unit_price * cart_item.quantity
				total_amount += line_total
				OrderItem.objects.create(
					order=order,
					product_id=cart_item.product_id,
					product_name=cart_item.product_name,
					unit_price=cart_item.unit_price,
					quantity=cart_item.quantity,
					line_total=line_total,
				)

			order.total_amount = total_amount
			order.save(update_fields=["total_amount", "updated_at"])
			cart.items.all().delete()

		return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
