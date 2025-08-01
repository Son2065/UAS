from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('api/tourist-spots', views.TouristSpotList.as_view(), name='tourist-spot-list'),
    path('api/tourist-spots/<int:id>', views.TouristSpotDetail.as_view(), name='tourist-spot-detail'),
    path('api/provinces', views.ProvinceList.as_view(), name='province-list'),
    path('api/provinces/<int:id>', views.ProvinceDetail.as_view(), name='province-detail'),
    path('api/cities', views.CityList.as_view(), name='city-list'),
    path('api/cities/<int:id>', views.CityDetail.as_view(), name='city-detail'),
    path('api/tourism-types', views.TourismTypeList.as_view(), name='tourism-type-list'),
    path('api/tourism-types/<int:id>', views.TourismTypeDetail.as_view(), name='tourism-type-detail'),
]