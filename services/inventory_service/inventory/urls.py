from django.urls import path
from rest_framework.routers import DefaultRouter

from inventory.views import InternalConsumeInventoryView, ProductViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"movements", StockMovementViewSet, basename="movements")

urlpatterns = router.urls + [
    path("internal/consume/", InternalConsumeInventoryView.as_view(), name="internal-consume"),
]
