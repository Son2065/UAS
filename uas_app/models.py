from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()


# Tambahan field profil provinsi
class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    capital_city = models.CharField(max_length=100, blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)
    area_km2 = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


# Tambahan field info kota/kabupaten
class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    is_capital = models.BooleanField(default=False)
    area_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('name', 'province')

    def __str__(self):
        return f'{self.name}, {self.province.name}'


# Kategori wisata diperluas
class TourismType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Tetap sama: Tempat Wisata
class TouristSpot(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    city = models.ForeignKey(City, related_name='tourist_spots', on_delete=models.CASCADE)
    tourism_type = models.ForeignKey(TourismType, on_delete=models.SET_NULL, null=True, blank=True)
    distance_from_city = models.DecimalField(max_digits=10, decimal_places=2, help_text="Dalam kilometer (km)")
    image = models.ImageField(upload_to='tourism_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='Aktif')
    user_create = models.ForeignKey(User, related_name='created_tourist_spots', on_delete=models.SET_NULL, null=True, blank=True)
    user_update = models.ForeignKey(User, related_name='updated_tourist_spots', on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.city.name}'
