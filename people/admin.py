from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id","name","image","created_at")
    search_fields = ("name","image")

