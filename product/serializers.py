from rest_framework import serializers
from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'status', 'price', 'quantity')
        read_only_fields = ('id', 'status')
    
    def create(self, validated_data):
        return super().create(validated_data)