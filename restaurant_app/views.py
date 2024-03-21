from django.shortcuts import render
from rest_framework import viewsets

from .models import Users, Restaurant, Restaurant_location, Restaurant_comment, Food, Food_comment
from .serializers import UsersSerializer, RestaurantSerializer, Restaurant_commentSerializer, \
    Restaurant_locationSerializer, FoodSerializer, Food_commentSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class Restaurant_locationViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_location.objects.all()
    serializer_class = Restaurant_locationSerializer


class Restaurant_commentViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_comment.objects.all()
    serializer_class = Restaurant_commentSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class Food_commentViewSet(viewsets.ModelViewSet):
    queryset = Food_comment.objects.all()
    serializer_class = Food_commentSerializer