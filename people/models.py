from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=32, blank=True, null=True)   # keep as string if CSV has messy ages
    gender = models.CharField(max_length=32, blank=True, null=True)
    image = models.CharField(max_length=512, blank=True, null=True)    # stores filename (e.g. 0001.png)
    embedding = models.TextField(blank=True, null=True)                # JSON string of embedding
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or self.image} ({self.pk})"
