# neighborhoods/admin.py
from django.contrib import admin
from .models import Neighborhood

@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'center_latitude', 'center_longitude')
    search_fields = ('name', 'city')
    list_filter = ('city',)