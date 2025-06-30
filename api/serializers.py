from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from uas_app.models import User, Province, City, TourismType, TouristSpot


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'is_active', 'is_admin', 'is_editor', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Kata sandi dan ulangi kata sandi tidak sama.'
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            is_admin=validated_data['is_admin'],
            is_editor=validated_data['is_editor'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError({'message': 'Status pengguna tidak aktif.'})
            else:
                raise ValidationError({'message': 'Kredensial tidak valid.'})
        else:
            raise ValidationError({'message': 'Harap isi nama pengguna dan kata sandi.'})
        return data


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
    user_create = serializers.StringRelatedField()
    user_update = serializers.StringRelatedField()

    class Meta:
        model = TouristSpot
        fields = [
            'id', 'name', 'description', 'address', 'city', 'tourism_type',
            'distance_from_city', 'image', 'status',
            'user_create', 'user_update', 'created_on', 'last_modified'
        ]
    