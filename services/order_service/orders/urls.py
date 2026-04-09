from django.urls import path

from orders.views import CheckoutView, OrderListView

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("checkout/", CheckoutView.as_view(), name="order-checkout"),
]
