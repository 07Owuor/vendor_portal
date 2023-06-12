from django.db import models
from django.utils import timezone


# Create your models here.
class Survey(models.Model):
    LOCATION = [
        ('KNE', 'KNE'),
        ('KLF', 'KLF'),
        ('Farm Star', 'Farm Star'),
        ('Sameer', 'Sameer')
    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=False, blank=False, choices=LOCATION, default='Sameer')
    mood = models.CharField(max_length=255, null=True, blank=True)
    mood_explanation = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False, blank=False)

    def __str__(self):
        return self.mood
