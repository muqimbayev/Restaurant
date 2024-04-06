

from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import viewsets,generics
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

class RestaurantSearchAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)

        user_location_data = get_user_location(self.request._request)  # Retrieve user's location
        latitude = user_location_data.get('latitude')
        longitude = user_location_data.get('longitude')

        if latitude is not None and longitude is not None:
            user_location = Point(longitude, latitude, srid=4326)  # Construct Point object for user location
            queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')
            # print(queryset)

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

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        user = authenticate(phone_number=request.POST.get('phone_number'),
                            password=request.POST.get('password'))
        if user:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('home_admin', )
            return redirect('home', )
        else:
            return HttpResponse("Invalid user")
    return render(request, "login.html")


def login_restaurant(request):
    if request.method == 'POST':
        res_user = authenticate(phone_number=request.POST.get('phone_number'),
                                password=request.POST.get('password'))
        if res_user:
            return redirect('')
        else:
            return HttpResponse('Invalid user')
    return  render(request, 'login_restaurant.html')

def sigin(request):
    if request.method == 'POST':
        new_user = Users.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone_number=request.POST.get('phone_number'),
        )
        new_user.set_password(request.POST.get('password'))
        new_user.save()
        return redirect('' )
    return render(request, 'signin.html')



def signin_restaurant(request):
    if request.method == "POST":
        new_restaurant = Restaurant.objects.create(
            name=request.POST.get('name'),
            username=request.POST.get('username'),
            phone_number=request.POST.get('phone_number'),
            type=request.POST.get('type')
        )
        new_restaurant.set_password(request.POST.get('password'))
        new_restaurant.save()
        return redirect('')
    return render(request, 'signin_restaurant.html')