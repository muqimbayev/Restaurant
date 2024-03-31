

from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect

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