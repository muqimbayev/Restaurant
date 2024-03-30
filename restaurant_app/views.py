import re

from django.db.models import F, Q
from django.db.models.functions import Power
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import viewsets, generics, filters, status
from rest_framework.filters import SearchFilter

from .models import *
from .serializers import *
import os
import requests
from fuzzywuzzy import process
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


@api_view(['GET'])
def get_user_location(request):
    maps_key = os.getenv('MAPS_KEY')
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={maps_key}'
    data = {}
    response = requests.post(url, json=data)
    location_data = response.json()
    latitude = location_data['location']['lat']
    longitude = location_data['location']['lng']

    def calculate_distances(locations, user_latitude, user_longitude):
        distances = []
        for location in locations:
            distance_in_meters = (((user_latitude - location['latitude']) ** 2 +
                                   (user_longitude - location['longitude']) ** 2) ** 0.5) * 111
            distances.append((location['name'], distance_in_meters))
        return distances

    locations_db = Restaurant_location.objects.all()

    locations = []
    for location in locations_db:
        locations.append({
            'name': location.restaurant.name,
            'latitude': location.latitude,
            'longitude': location.longitude
        })

    restaurant_info = calculate_distances(locations, latitude, longitude)
    info = []
    for restaurant, distance in sorted(restaurant_info, key=lambda x: x[1]):
        loc = Restaurant_location.objects.get(restaurant_id__name=restaurant)
        restaurant_info = {
            'name': restaurant,
            'region': loc.region,
            'district': loc.district,
            'address': loc.address,
        }

        info.append(restaurant_info)

    return Response(info)


# class RestaurantListView(generics.ListAPIView):
#     serializer_class = RestaurantSerializer
#
#     # fuzzy_fields = {'name': 2, 'description': 1, 'address': 1}
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING)
#         ]
#     )

class RestaurantSearchAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            search_query_lower = search_query.lower()
            search_set = set(search_query_lower)

            filtered_restaurants = []

            for restaurant in queryset:

                restaurant_name = restaurant.name.replace("<", "").replace(">", "").capitalize()
                restaurant_name_lower = restaurant_name.lower()
                restaurant_name_set = set(restaurant_name_lower)

                search_set_intersection = restaurant_name_set.intersection(search_set)

                if len(search_set_intersection) >= len(search_set) / 2:
                    filtered_restaurants.append(restaurant)

            return filtered_restaurants
        else:
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
