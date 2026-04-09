from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=3, default_retry_delay=15)
def send_order_created_email(self, order_id: int, total_amount: str, user_id: int):
    subject = f"[Order Created] Order #{order_id}"
    body = (
        f"A new order was created.\\n"
        f"Order ID: {order_id}\\n"
        f"User ID: {user_id}\\n"
        f"Total: {total_amount}"
    )

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ORDER_ALERT_EMAIL],
            fail_silently=False,
        )
    except Exception as exc:  # pragma: no cover - depends on SMTP runtime
        raise self.retry(exc=exc)
