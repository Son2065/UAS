from rest_framework import serializers
from uas_app.models import User, Province, City, TourismType, TouristSpot

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'abbreviation', 'capital_city', 'population', 'area_km2']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'is_capital', 'area_code', 'latitude', 'longitude', 'population']


class TourismTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismType
        fields = ['id', 'name', 'description', 'is_active']


class TouristSpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TouristSpot
        fields = [
            'id', 'name', 'description', 'address', 'city', 'tourism_type',
            'distance_from_city', 'image', 'status', 'created_on', 'last_modified'
        ]
    