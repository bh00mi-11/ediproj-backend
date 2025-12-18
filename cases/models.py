from django.db import models

class Case(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    birthdate = models.DateField()
    contact_number = models.CharField(max_length=20)
    notification_email = models.EmailField()
    last_seen_location = models.CharField(max_length=200)
    additional_details = models.TextField()

    def __str__(self):
        return self.full_name
