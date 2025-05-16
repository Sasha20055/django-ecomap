from django import forms
from .models import Location, WasteType, LocationWaste, Review

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'latitude', 'longitude']

class WasteTypeForm(forms.ModelForm):
    class Meta:
        model = WasteType
        fields = ['name', 'description']

class LocationWasteForm(forms.ModelForm):
    class Meta:
        model = LocationWaste
        fields = ['location', 'waste_type']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['location', 'rating', 'comment']