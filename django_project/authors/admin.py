"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Author


@admin.register(Author)
class BookAdmin(admin.ModelAdmin):
    """
    Admin Model Settings
    """
    list_display = ('first_name', 'last_name')
