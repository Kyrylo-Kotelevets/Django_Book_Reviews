"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Genre


@admin.register(Genre)
class BookAdmin(admin.ModelAdmin):
    """
    Genre Model Settings
    """
    list_display = ('name',)
