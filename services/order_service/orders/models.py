from django.db import models


class Order(models.Model):
	STATUS_PENDING = "PENDING"
	STATUS_CONFIRMED = "CONFIRMED"
	STATUS_FAILED = "FAILED"
	STATUS_CHOICES = (
		(STATUS_PENDING, "Pending"),
		(STATUS_CONFIRMED, "Confirmed"),
		(STATUS_FAILED, "Failed"),
	)

	user_id = models.BigIntegerField(db_index=True)
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
	total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return f"Order(id={self.id}, user={self.user_id}, status={self.status})"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
	product_id = models.BigIntegerField()
	product_name = models.CharField(max_length=255)
	unit_price = models.DecimalField(max_digits=12, decimal_places=2)
	quantity = models.PositiveIntegerField()
	line_total = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return f"OrderItem(order={self.order_id}, product={self.product_id}, qty={self.quantity})"
