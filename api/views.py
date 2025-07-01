from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uas_app.models import User, TouristSpot, Province, City, TourismType
from api.serializers import (TouristSpotSerializer, ProvinceSerializer, CitySerializer, TourismTypeSerializer)
from django.http import JsonResponse

class TouristSpotList(APIView):

    def get(self, request, *args, **kwargs):
        spots = TouristSpot.objects.all()
        serializer = TouristSpotSerializer(spots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'tourism_type': request.data.get('tourism_type'),
            'distance_from_city': request.data.get('distance_from_city'),
            'image': request.data.get('image'),
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

class ProvinceList(APIView):

    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
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

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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

    def get(self, request):
        types = TourismType.objects.all()
        serializer = TourismTypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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