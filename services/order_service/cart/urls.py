from django.urls import path

from cart.views import CartItemCreateListView, CartItemDetailView, CartSummaryView

urlpatterns = [
    path("", CartSummaryView.as_view(), name="cart-summary"),
    path("items/", CartItemCreateListView.as_view(), name="cart-item-list-create"),
    path("items/<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail"),
]
