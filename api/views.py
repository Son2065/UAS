from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from uas_app.models import User, TouristSpot, Province, City, TourismType
from api.serializers import (
    TouristSpotSerializer, RegisterUserSerializer, LoginSerializer,
    ProvinceSerializer, CitySerializer, TourismTypeSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsEditorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_editor

class IsAdminOrEditorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_admin or request.user.is_editor
        )

class TouristSpotList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrEditorUser]

    def get(self, request, *args, **kwargs):
        spots = TouristSpot.objects.all()
        serializer = TouristSpotSerializer(spots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': 'Hanya admin yang dapat menambahkan'}, status=status.HTTP_403_FORBIDDEN)
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'tourism_type': request.data.get('tourism_type'),
            'distance_from_city': request.data.get('distance_from_city'),
            'image': request.data.get('image'),
            'user_create': request.user.id if request.user.is_authenticated else None,
        }
        serializer = TouristSpotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Wisata berhasil ditambahkan',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TouristSpotDetail(APIView):

    def get_object(self, id):
        try:
            return TouristSpot.objects.get(id=id)
        except TouristSpot.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = TouristSpotSerializer(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Wisata ditemukan',
            'data': serializer.data
        })

    def put(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'address' : request.data.get('address'),
            'city' : request.data.get('city'),
            'tourism_type' : request.data.get('tourism_type'),
            'distance_from_city': request.data.get('distance_from_city'),
            'image': request.data.get('image'),
            'status': request.data.get('status'),
        }
        serializer = TouristSpotSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(user_update=request.user if request.user.is_authenticated else None)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Wisata berhasil diupdate',
                'data': serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Data wisata berhasil dihapus'
        })

class RegisterUser(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Pendaftaran akun berhasil',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Pendaftaran akun gagal',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'status': 200,
            'message': 'Login berhasil.',
            'data': {
                'token': token.key,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'is_editor': user.is_editor
            }
        })

class ProvinceList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrEditorUser]

    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_admin:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': 'Hanya admin yang dapat menambahkan'}, status=status.HTTP_403_FORBIDDEN)
        
        data = {
            'name': request.data.get('name'),
            'abbreviation': request.data.get('abbreviation'),
            'capital_city': request.data.get('capital_city'),
            'population': request.data.get('population'),
            'area_km2': request.data.get('area_km2'),
        }
        serializer = ProvinceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Provinsi berhasil ditambahkan',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProvinceDetail(APIView):
    def get_object(self, id):
        try:
            return Province.objects.get(id=id)
        except Province.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Provinsi tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProvinceSerializer(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Provinsi ditemukan',
            'data': serializer.data
        })

    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Provinsi tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'name': request.data.get('name'),
            'abbreviation': request.data.get('abbreviation'),
            'capital_city': request.data.get('capital_city'),
            'population': request.data.get('population'),
            'area_km2': request.data.get('area_km2'),
        }
        serializer = ProvinceSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data provinsi berhasil diupdate',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Provinsi tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Data provinsi berhasil dihapus'
            })


class CityList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrEditorUser]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': 'Hanya admin yang dapat menambahkan'}, status=status.HTTP_403_FORBIDDEN)
        
        data = {
            'name': request.data.get('name'),
            'province': request.data.get('province'),
            'is_capital': request.data.get('is_capital'),
            'area_code': request.data.get('area_code'),
            'latitude': request.data.get('latitude'),
            'longitude': request.data.get('longitude'),
            'population': request.data.get('population'),
        }
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Kota berhasil ditambahkan',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDetail(APIView):
    def get_object(self, id):
        try:
            return City.objects.get(id=id)
        except City.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Kota tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CitySerializer(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Kota ditemukan',
            'data': serializer.data
        })

    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Kota tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'name': request.data.get('name'),
            'province': request.data.get('province'),
            'is_capital': request.data.get('is_capital'),
            'area_code': request.data.get('area_code'),
            'latitude': request.data.get('latitude'),
            'longitude': request.data.get('longitude'),
            'population': request.data.get('population'),
        }
        serializer = CitySerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data kota berhasil diperbarui',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Kota tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Data kota berhasil dihapus'
        })


class TourismTypeList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        types = TourismType.objects.all()
        serializer = TourismTypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': 'Hanya admin yang dapat menambahkan'}, status=status.HTTP_403_FORBIDDEN)
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'is_active': request.data.get('is_active'),
        }
        serializer = TourismTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Jenis wisata berhasil ditambahkan',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TourismTypeDetail(APIView):
    def get_object(self, id):
        try:
            return TourismType.objects.get(id=id)
        except TourismType.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Jenis wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = TourismTypeSerializer(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Jenis wisata ditemukan',
            'data': serializer.data
        })

    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Jenis wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'is_active': request.data.get('is_active'),
        }
        serializer = TourismTypeSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data jenis wisata berhasil diperbarui',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Jenis wisata tidak ditemukan',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Data jenis wisata berhasil dihapus'
        })

class ProvinceFilterAPI(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'abbreviation', 'capital_city']
    ordering_fields = ['name', 'population', 'area_km2']


class CityFilterAPI(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'province', 'is_capital']
    ordering_fields = ['name', 'population']


class TourismTypeFilterAPI(generics.ListAPIView):
    queryset = TourismType.objects.all()
    serializer_class = TourismTypeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'is_active']
    ordering_fields = ['name', 'is_active']


class TouristSpotFilterAPI(generics.ListAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'address', 'city', 'tourism_type', 'status']
    ordering_fields = ['name', 'city', 'distance_from_city', 'created_on']