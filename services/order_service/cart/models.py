from django.db import models


class Cart(models.Model):
	user_id = models.BigIntegerField(unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Cart(user_id={self.user_id})"


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
	product_id = models.BigIntegerField()
	product_name = models.CharField(max_length=255)
	unit_price = models.DecimalField(max_digits=12, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("cart", "product_id")

	@property
	def line_total(self):
		return self.unit_price * self.quantity

	def __str__(self):
		return f"CartItem(cart={self.cart_id}, product={self.product_id}, qty={self.quantity})"
