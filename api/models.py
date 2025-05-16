from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations'
    )

class WasteType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class LocationWaste(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='wastes')
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('location', 'waste_type')

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
