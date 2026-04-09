from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer


def get_user_id(request) -> int:
	return int(request.user.id)


def get_or_create_cart(user_id: int) -> Cart:
	cart, _ = Cart.objects.get_or_create(user_id=user_id)
	return cart


class CartSummaryView(APIView):
	def get(self, request):
		user_id = get_user_id(request)
		cart = Cart.objects.prefetch_related("items").filter(user_id=user_id).first()
		if not cart:
			cart = Cart.objects.create(user_id=user_id)
		return Response(CartSerializer(cart).data)


class CartItemCreateListView(generics.GenericAPIView):
	serializer_class = CartItemSerializer

	def get(self, request):
		user_id = get_user_id(request)
		cart = get_or_create_cart(user_id)
		items = cart.items.all().order_by("-updated_at")
		return Response(self.get_serializer(items, many=True).data)

	def post(self, request):
		user_id = get_user_id(request)
		cart = get_or_create_cart(user_id)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		product_id = serializer.validated_data["product_id"]
		defaults = {
			"product_name": serializer.validated_data["product_name"],
			"unit_price": serializer.validated_data["unit_price"],
			"quantity": serializer.validated_data["quantity"],
		}
		item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults=defaults)
		if not created:
			item.product_name = defaults["product_name"]
			item.unit_price = defaults["unit_price"]
			item.quantity += defaults["quantity"]
			item.save()

		return Response(self.get_serializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.GenericAPIView):
	serializer_class = CartItemSerializer

	def patch(self, request, item_id: int):
		user_id = get_user_id(request)
		cart = get_or_create_cart(user_id)
		item = get_object_or_404(CartItem, id=item_id, cart=cart)
		serializer = self.get_serializer(item, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def delete(self, request, item_id: int):
		user_id = get_user_id(request)
		cart = get_or_create_cart(user_id)
		item = get_object_or_404(CartItem, id=item_id, cart=cart)
		item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
