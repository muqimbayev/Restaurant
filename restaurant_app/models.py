from django.db import models
from django.contrib.auth.hashers import make_password

class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15) 
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.password: 
            self.password = make_password(self.password)  
        super(Users, self).save(*args, **kwargs)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    type = models.CharField(max_length=15)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.password: 
            self.password = make_password(self.password)  
        super(Restaurant, self).save(*args, **kwargs)


class Restaurant_location(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class Restaurant_comment(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    score = models.FloatField()


class Food(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.CharField(max_length=255)


class Food_comment(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    score = models.FloatField()
