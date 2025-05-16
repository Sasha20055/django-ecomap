from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Location, WasteType, LocationWaste, Review


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # перечислите поля, которые хотите отдавать/принимать
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'patronymic', 'role']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name','address','latitude','longitude','added_by']
        read_only_fields = ['added_by']

class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = '__all__'

class LocationWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWaste
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
