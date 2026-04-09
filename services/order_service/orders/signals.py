from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.tasks import send_order_created_email


@receiver(post_save, sender=Order)
def order_created_signal(sender, instance: Order, created: bool, **kwargs):
    if created and instance.status == Order.STATUS_CONFIRMED:
        send_order_created_email.delay(instance.id, str(instance.total_amount), instance.user_id)
