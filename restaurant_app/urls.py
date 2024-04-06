from rest_framework import routers
from django.urls import path, include

from restaurant_app import views
from restaurant_app.views import login, home, sigin, login_restaurant, signin_restaurant

from restaurant_app.views import RestaurantSearchAPIView

router = routers.DefaultRouter()
router.register(r'User', views.UserViewSet)
router.register(r'restaurant', views.RestaurantViewSet)
router.register(r'food', views.FoodViewSet)
router.register(r'food_comment', views.Food_commentViewSet)
router.register(r'restaurant_comment', views.Restaurant_commentViewSet)
router.register(r'restaurant_location', views.Restaurant_locationViewSet)
router.register(r'restaurant_images', views.Restaurant_imagesViewSet)
router.register(r'food_images', views.Food_imagesViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('signin', sigin, name='sigin'),
    path('login_restaurant', login_restaurant, name='login_restaurant'),
    path('signin_restaurant', signin_restaurant, name='signin_restaurant'),
    path('reduc', include(router.urls)),
    path('location/', views.get_user_location, name='location'),
    path('restaurants/', RestaurantSearchAPIView.as_view(), name='restaurant-list'),
]

