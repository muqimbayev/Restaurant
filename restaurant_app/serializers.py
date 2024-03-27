from rest_framework import serializers
from .models import *

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name', 'username', 'phone_number', 'type')
        extra_kwargs = {
            'password': {'write_only': True},
        }

class Restaurant_commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_comment
        fields = '__all__'

class Restaurant_locationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_location
        fields = '__all__'

class Food_commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_comment
        fields = '__all__'

class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_images
        fields = '__all__'

class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_images
        fields = '__all__'
