from django.shortcuts import render

from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
import os
import requests
from rest_framework.response import Response

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

class Food_imagesViewSet(viewsets.ModelViewSet):
    queryset = Food_images.objects.all()
    serializer_class = FoodImageSerializer

class Restaurant_imagesViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_images.objects.all()
    serializer_class = RestaurantImageSerializer


import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant_location
import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant_location

@api_view(['GET'])
def get_user_location(request):
    maps_key = os.getenv('MAPS_KEY')
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={maps_key}'
    data = {}
    response = requests.post(url, json=data)
    location_data = response.json()
    user_latitude = location_data['location']['lat']
    user_longitude = location_data['location']['lng']
    print(user_latitude, user_longitude)

    def calculate_distances(locations, user_latitude, user_longitude):
        distances = []
        for location in locations:
            distance_in_meters = (((user_latitude - location['latitude']) ** 2 + (
                    user_longitude - location['longitude']) ** 2) ** 0.5) * 1110
            distances.append((distance_in_meters, location['name']))
        return sorted(distances)  # Distance bo'yicha tartiblash

    locations_db = Restaurant_location.objects.all()

    locations = []
    for location in locations_db:
        locations.append({
            'name': location.restaurant.name,
            'latitude': location.latitude,
            'longitude': location.longitude
        })

    restaurant_info = calculate_distances(locations, user_latitude, user_longitude)

    info = []
    for distance, restaurant in restaurant_info:
        restaurant_obj = Restaurant_location.objects.filter(restaurant__name=restaurant).first()
        if restaurant_obj:
            restaurant_info = {
                'name': restaurant,
                'region': restaurant_obj.region,
                'district': restaurant_obj.district,
                'address': restaurant_obj.address,
            }
            info.append(restaurant_info)

    return Response(info)
