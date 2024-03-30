from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Restaurant_comment)
admin.site.register(Restaurant_location)
admin.site.register(Food_comment)

