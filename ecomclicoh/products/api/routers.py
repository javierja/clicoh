from rest_framework.routers import DefaultRouter
from products.api.viewsets import ProductViewSet, OrderViewSet, OrderDetailViewSet, OrderTotal, OrderTotalUsd

router=DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'ordersdetail', OrderDetailViewSet, basename='orderdetail')
router.register(r'get-total', OrderTotal, basename='get-total')
router.register(r'get-total-usd', OrderTotalUsd, basename='get-total-usd')

urlpatterns=router.urls