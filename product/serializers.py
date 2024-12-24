from rest_framework import serializers
from .models import Product
from my_auth.serializers import UserSerializer
from typing import Dict


# serializing product to show in response
class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False)
    class Meta:
        model = Product
        fields = ('id','name','price','description','created_by','created_at') # fields to be serialized in the response


    
# serializer for creation and update a product     
class ProductCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name','price','description')


    # validate positive price before database schema validation
    def validate_price(self, value:float):
        if value <= 0:
            raise serializers.ValidationError('Price cannot be negative or zero')
        return value
    
    # for saving or updating a product 
    def create(self, validated_data:Dict):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    



    
