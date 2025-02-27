from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'total_amount_to_paid', 'paid_amount', 'odd_money', 'created_at', 'processed_date')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'order', 'quantity', 'total_price')
        read_only_fields = ('id', 'total_price', 'order') 

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs.get('quantity', 0)

        if not product.status:
            raise serializers.ValidationError('Product status is False, you can’t buy this product')

        if product.quantity < quantity:
            raise serializers.ValidationError('Fewer items in stock')

        return attrs

class OrderPaidSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, required=True, write_only=True)
    class Meta:
        model = Order
        fields = ('id', 'amount')

    def validate(self, attrs):
        amount = attrs['amount']

        if amount <= 0:
            raise serializers.ValidationError('The amount must be greater than 0')

        if self.instance and self.instance.total_amount_to_paid > amount:
            raise serializers.ValidationError({'message':'The amount is less than the required payment', 'shoudl be':self.instance.total_amount_to_paid, 'odd_money': amount})

        return attrs
