from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        read_only_fields = ('password',)
        
    password = serializers.CharField(min_length=8, max_length=100, required=True, write_only=True)
    
    def validate(self, attrs):
        password = attrs['password']
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                {'password': {"letter_numbers": 'The password must contain letters and numbers'}}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        Token.objects.create(user = user)
        return user