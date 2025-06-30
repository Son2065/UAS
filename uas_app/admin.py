from django.contrib import admin
from uas_app.models import User, Province, City, TourismType, TouristSpot

# Register your models here.
admin.site.register(User)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(TourismType)
admin.site.register(TouristSpot)