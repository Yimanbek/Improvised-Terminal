from django.shortcuts import render
from rest_framework import permissions, generics, viewsets, mixins, status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, OrderPaidSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderCreateViews(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

class OrderItemViews(viewsets.GenericViewSet, 
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.AllowAny, permissions.IsAdminUser)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.order.remove_amount_from_order(instance.total_price)
        instance.product.rollback_product(instance.quantity)
        return super().destroy(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        instance.order.remove_amount_from_order(instance.total_price)
        instance.product.rollback_product(instance.quantity)
        response = serializer.save()
        return response
    
    @action(detail=False, methods=['post'], url_path='add-product/(?P<order_id>\\d+)')
    def add_product(self, request, order_id=None):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = OrderItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class OrderViews(viewsets.GenericViewSet, 
                 mixins.RetrieveModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderPaidSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail = True, methods = ['post'])
    def paid(self, request, pk = None):
        order = self.get_object()
        serializer = OrderPaidSerializer(data = request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            data = order.paid_process(amount)
            order.create_transaction()

            if isinstance(data, Order):
                data = OrderSerializer(data).data
            return Response(data, status=200)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderSerializer(instance)
        return Response(serializer.data)
