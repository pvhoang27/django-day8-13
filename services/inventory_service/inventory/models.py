from django.db import models


class Product(models.Model):
	sku = models.CharField(max_length=64, unique=True)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	stock_quantity = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-updated_at",)

	def __str__(self):
		return f"{self.sku} - {self.name}"


class StockMovement(models.Model):
	MOVEMENT_IN = "IN"
	MOVEMENT_OUT = "OUT"
	MOVEMENT_ADJUST = "ADJUST"
	MOVEMENT_CHOICES = (
		(MOVEMENT_IN, "Stock In"),
		(MOVEMENT_OUT, "Stock Out"),
		(MOVEMENT_ADJUST, "Manual Adjust"),
	)

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
	movement_type = models.CharField(max_length=8, choices=MOVEMENT_CHOICES)
	quantity = models.IntegerField()
	note = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return f"{self.product.sku} | {self.movement_type} | {self.quantity}"
