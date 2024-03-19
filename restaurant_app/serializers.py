from rest_framework import serializers
from .models import *

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'phone_number')

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

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
