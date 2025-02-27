from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderCreateViews, OrderItemViews, OrderViews

router = DefaultRouter()
router.register(r'order-item', OrderItemViews, basename='order_item')
router.register(r'order-paid', OrderViews, basename='order_paid')

urlpatterns = [
    path('order-create/', OrderCreateViews.as_view()),
    path('', include(router.urls)),
]