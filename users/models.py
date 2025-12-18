from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("family", "Family"),
        ("ngo", "NGO"),
        ("volunteer-normal", "Volunteer Normal"),
        ("volunteer-police", "Volunteer Police"),
        ("admin-role", "Admin"),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="family")
